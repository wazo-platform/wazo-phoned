# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from functools import wraps

from flask import current_app
from flask import request
from flask_restful import Resource
from flask_restful import abort
from netaddr import IPNetwork, IPAddress

logger = logging.getLogger(__name__)


def verify_remote_addr(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        remote_addr = request.remote_addr
        if not remote_addr:
            abort(403)

        networks = current_app.config['authorized_subnets']
        for network in networks:
            if IPAddress(remote_addr) in IPNetwork(network):
                return func(*args, **kwargs)

        abort(403)
    return wrapper


class AuthResource(Resource):
    method_decorators = [verify_remote_addr]
