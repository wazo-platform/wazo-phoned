# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import requests

from flask import current_app
from time import time

from xivo_auth_client import Client

logger = logging.getLogger(__name__)


def verify_token(token):
    try:
        token_is_valid = client().token.is_valid(token)
    except requests.RequestException as e:
        auth_host = current_app.config['auth']['host']
        auth_port = current_app.config['auth']['port']
        message = 'Could not connect to authentication server on {host}:{port}: {error}'.format(host=auth_host,
                                                                                                port=auth_port,
                                                                                                error=e)
        logger.exception(message)
        return {
            'reason': [message],
            'timestamp': [time()],
            'status_code': 503,
        }, 503
    return token_is_valid


def client():
    auth_host = current_app.config['auth']['host']
    auth_port = current_app.config['auth']['port']
    auth_secret = current_app.config['auth']['secret']
    return Client(auth_host, auth_port, username='xivo-dird-phoned', password=auth_secret)
