# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.rest_api_helpers import APIException


class WazoAuthConnectionError(APIException):
    def __init__(self):
        msg = 'Connection to Wazo Auth failed'
        super().__init__(503, msg, 'auth-unreachable')


class WazoDirdConnectionError(APIException):
    def __init__(self):
        msg = 'Connection to Wazo Dird failed'
        super().__init__(503, msg, 'dird-unreachable')


class NoSuchUser(APIException):
    def __init__(self, uuid):
        user_uuid = str(uuid)
        msg = f'No such user: "{user_uuid}"'
        details = {'uuid': user_uuid}
        super().__init__(404, msg, 'unknown-user', details)


class NoSuchDevice(APIException):
    def __init__(self, device_id):
        msg = f'No such device: "{device_id}"'
        details = {'device_id': device_id}
        super().__init__(404, msg, 'unknown-device', details)


class NowhereToRouteEndpoint(APIException):
    def __init__(self, endpoint_name):
        msg = f'Nowhere to route endpoint: "{endpoint_name}"'
        details = {'endpoint_name': endpoint_name}
        super().__init__(400, msg, 'nowhere-to-route-endpoint', details)


class NoSuchEndpoint(APIException):
    def __init__(self, endpoint_name):
        msg = f'No such endpoint: "{endpoint_name}"'
        details = {'endpoint_name': endpoint_name}
        super().__init__(404, msg, 'unknown-endpoint', details)
