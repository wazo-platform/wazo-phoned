# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from requests.exceptions import RequestException


class WazoAuthConnectionError(RequestException):

    code = 503

    def __str__(self):
        return 'Connection to XiVO Auth failed'


class WazoDirdConnectionError(RequestException):

    code = 503

    def __str__(self):
        return 'Connection to XiVO Dird failed'
