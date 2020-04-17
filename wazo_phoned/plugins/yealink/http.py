# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import request
import logging

from wazo_phoned.auth_remote_addr import AuthResource
from wazo_phoned.plugin_helpers.client.http import ClientLookup
from wazo_phoned.plugin_helpers.client.schema import UserForwardSchema, UserServiceSchema

logger = logging.getLogger(__name__)


class Lookup(ClientLookup):

    content_type = 'text/xml; charset=utf-8'
    template = 'yealink_results.jinja'


class DNDUserService(AuthResource):

    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    def get(self):
        args = UserServiceSchema().load(request.args)
        user_uuid = args['user_uuid']
        enabled = args['enabled']
        logger.debug('DND hit BEFORE')

        self._service.update_dnd(user_uuid, enabled)
        logger.debug('DND hit AFTER')

        return '', 200


class UnconditionalForwardUserService(AuthResource):

    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    def get(self):
        args = UserForwardSchema().load(request.args)
        user_uuid = args['user_uuid']
        destination = args['destination']
        enabled = args['enabled']

        self._service.update_forward_unconditional(user_uuid, destination, enabled)
        return '', 200


class NoAnswerForwardUserService(AuthResource):

    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    def get(self):
        args = UserForwardSchema().load(request.args)
        user_uuid = args['user_uuid']
        destination = args['destination']
        enabled = args['enabled']

        self._service.update_forward_noanswer(user_uuid, destination, enabled)
        return '', 200


class BusyForwardUserService(AuthResource):

    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    def get(self):
        args = UserForwardSchema().load(request.args)
        user_uuid = args['user_uuid']
        destination = args['destination']
        enabled = args['enabled']

        self._service.update_forward_busy(user_uuid, destination, enabled)
        return '', 200
