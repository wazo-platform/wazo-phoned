# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from functools import wraps

from flask import current_app
from flask import request
from flask_restful import Resource
from flask_restful import abort
from netaddr import IPNetwork, IPAddress

from xivo import mallow_helpers
from xivo import rest_api_helpers

logger = logging.getLogger(__name__)


def verify_remote_addr(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        remote_addr = request.remote_addr
        if not remote_addr:
            logging.debug('Could not identify remote address. Aborting...')
            abort(403)

        networks = current_app.config['authorized_subnets']
        for network in networks:
            if IPAddress(remote_addr) in IPNetwork(network):
                return func(*args, **kwargs)

        logging.info(
            'Remote address %s is not in authorized subnets. Aborting...', remote_addr
        )
        abort(403)

    return wrapper


class ErrorCatchingResource(Resource):
    method_decorators = [
        mallow_helpers.handle_validation_exception,
        rest_api_helpers.handle_api_exception,
    ] + Resource.method_decorators


class AuthResource(ErrorCatchingResource):
    method_decorators = [verify_remote_addr] + ErrorCatchingResource.method_decorators
