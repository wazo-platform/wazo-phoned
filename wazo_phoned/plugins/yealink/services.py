# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import time

from requests.exceptions import RequestException
from wazo_phoned.plugin_helpers.client.exceptions import NoSuchUser

from flask import (
    render_template,
    Response,
    request
)

logger = logging.getLogger(__name__)

USER_EVENT_TIMEOUT = 10


class YealinkService:
    def __init__(self, amid_client, confd_client):
        self.amid = amid_client
        self.confd = confd_client
        self._waiting_for_event = {}

    def update_dnd(self, user_uuid, enabled):
        user = self._find_user(user_uuid)
        self._clean_old_user_events()

        current_dnd = user['services'].get('dnd', {}).get('enabled', False)
        if current_dnd != enabled and user_uuid not in self._waiting_for_event:
            self._waiting_for_event[user_uuid] = time.time()
            self.confd.users(user_uuid).update_service('dnd', {'enabled': enabled})

    def notify_dnd(self, user_uuid, enabled):
        user = self._find_user(user_uuid)
        self._waiting_for_event.pop(user_uuid, None)
        for line in user['lines']:
            endpoint = line.get('endpoint_sip')
            if endpoint:
                endpoint_name = endpoint.get('name')
                if enabled:
                    self._send_notify(endpoint_name, 'DNDOn')
                    logger.debug('Sending DNDOn to phone "%s"', endpoint_name)
                else:
                    self._send_notify(endpoint_name, 'DNDOff')
                    logger.debug('Sending DNDOff to phone "%s"', endpoint_name)

    def hold_call(self, endpoint_name):
        logger.debug('Holding endpoint %s', endpoint_name)
        self._send_notify(endpoint_name, 'F_HOLD')

    def unhold_call(self, endpoint_name):
        logger.debug('Unholding endpoint %s', endpoint_name)
        self._send_notify(endpoint_name, 'F_HOLD')

    def answer_call(self, endpoint_name):
        logger.debug('Answering call on endpoint %s', endpoint_name)
        self._send_notify(endpoint_name, 'ANSWER')

    def view_authentication(self):
        response_rendered = render_template(
            'yealink_authentication.jinja',
            hostname = request.host_url.replace("http", "https")
        )

        return Response(response_rendered, content_type='text/xml; charset=utf-8', status=200)

    def authenticate(self, provcode):
        if not provcode:
            return '', 404

        response = self.confd.lines.list(provisioning_code=provcode, recurse=True)
        if response['total'] < 1:
            return '', 404

        registrar = self.confd.registrars.get(response['items'][0]['registrar'])
        endpoint_sip_id = response['items'][0]['endpoint_sip']['id']
        caller_id_name = response['items'][0]['caller_id_name']
        line = self.confd.endpoints_sip.get(endpoint_sip_id)
        line['caller_id_name'] = caller_id_name
        response_rendered = render_template(
            'yealink_account.jinja',
            line = line,
            registrar = registrar
        )

        return Response(response_rendered, content_type='text/xml; charset=utf-8', status=200)

    def _send_notify(self, line, value):
        self.amid.action(
            'PJSIPNotify',
            {
                'Endpoint': line,
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    f'Content=key={value}',
                ],
            },
        )

    def _find_user(self, user_uuid):
        try:
            user = self.confd.users.get(user_uuid)
        except RequestException as e:
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)
            if status_code == 404:
                raise NoSuchUser(user_uuid)
            raise
        return user

    def _clean_old_user_events(self):
        self._waiting_for_event = {
            user_uuid: event_time
            for user_uuid, event_time in self._waiting_for_event.items()
            if time.time() - event_time < USER_EVENT_TIMEOUT
        }
