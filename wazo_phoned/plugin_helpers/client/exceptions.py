# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
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
        msg = 'No such user: "{}"'.format(user_uuid)
        details = {'uuid': user_uuid}
        super().__init__(404, msg, 'unknown-user', details)
