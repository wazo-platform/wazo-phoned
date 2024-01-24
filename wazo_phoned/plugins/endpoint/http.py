# Copyright 2020-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.auth_verifier import required_acl

from wazo_phoned.auth import TokenAuthResource


class EndpointHoldStartResource(TokenAuthResource):
    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    @required_acl('phoned.endpoints.{endpoint_name}.hold.start')
    def put(self, endpoint_name):
        self._service.hold(endpoint_name)
        return '', 204


class EndpointHoldStopResource(TokenAuthResource):
    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    @required_acl('phoned.endpoints.{endpoint_name}.hold.stop')
    def put(self, endpoint_name):
        self._service.unhold(endpoint_name)
        return '', 204


class EndpointAnswerResource(TokenAuthResource):
    def __init__(self, service, *args, **kwargs):
        super().__init__()
        self._service = service

    @required_acl('phoned.endpoints.{endpoint_name}.answer')
    def put(self, endpoint_name):
        self._service.answer(endpoint_name)
        return '', 204
