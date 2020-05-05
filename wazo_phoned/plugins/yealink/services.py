# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from requests.exceptions import RequestException
from wazo_phoned.plugin_helpers.client.exceptions import NoSuchUser


class YealinkService:
    def __init__(self, amid_client, confd_client):
        self.amid = amid_client
        self.confd = confd_client

    def update_dnd(self, user_uuid, enabled):
        try:
            self.confd.users(user_uuid).update_service('dnd', {'enabled': enabled})
        except RequestException as e:
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)
            if status_code == 404:
                raise NoSuchUser(user_uuid)
            raise

    def notify_dnd(self, user_uuid, enabled):
        lines = self._find_lines(user_uuid)
        for line in lines:
            endpoint = line.get('endpoint_sip')
            if endpoint:
                endpoint_name = endpoint.get('name')
                if enabled:
                    self._send_notify(endpoint_name, 'DNDOn')
                else:
                    self._send_notify(endpoint_name, 'DNDOff')

    def _send_notify(self, line, value):
        self.amid.action(
            'PJSIPNotify',
            {
                'Endpoint': line,
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key={}'.format(value),
                ],
            },
        )

    def _find_lines(self, user_uuid):
        try:
            user = self.confd.users.get(user_uuid)
        except RequestException as e:
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)
            if status_code == 404:
                raise NoSuchUser(user_uuid)
            raise
        return user['lines']
