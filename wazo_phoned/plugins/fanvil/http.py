# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.auth import AuthResource
from wazo_phoned.plugin_helpers.client.http import ClientInput, ClientLookup


class Input(ClientInput):
    content_type = 'text/xml; charset=utf-8'
    template = 'fanvil_input.jinja'


class Lookup(ClientLookup):
    MAX_ITEM_PER_PAGE = 16
    content_type = 'text/xml; charset=utf-8'
    template = 'fanvil_results.jinja'


class LookupV2(ClientLookup):
    MAX_ITEM_PER_PAGE = None
    content_type = 'text/xml; charset=utf-8'
    template = 'fanvil_results_v2.jinja'


class DNDUserServiceEnable(AuthResource):
    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    def get(self, user_uuid):
        self._service.update_dnd(user_uuid, True)

        return '', 200


class DNDUserServiceDisable(AuthResource):
    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    def get(self, user_uuid):
        self._service.update_dnd(user_uuid, False)

        return '', 200
