# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from functools import wraps

from flask import current_app, request
from flask_restful import Resource, abort
from netaddr import IPAddress, IPNetwork
from werkzeug.local import LocalProxy as Proxy
from xivo import mallow_helpers, rest_api_helpers
from xivo.auth_verifier import AuthVerifier, required_tenant

from wazo_phoned.exceptions import MasterTenantNotInitialized
from wazo_phoned.http_server import app

auth_verifier = AuthVerifier()

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


class TokenAuthResource(ErrorCatchingResource):
    method_decorators = [
        auth_verifier.verify_tenant,
        auth_verifier.verify_token,
    ] + ErrorCatchingResource.method_decorators


def required_master_tenant():
    return required_tenant(master_tenant_uuid)


def init_master_tenant(token):
    tenant_uuid = token['metadata']['tenant_uuid']
    app.config['auth']['master_tenant_uuid'] = tenant_uuid
    logger.debug('Initiated master tenant UUID: %s', tenant_uuid)


def get_master_tenant_uuid():
    if not app:
        raise Exception('Flask application not configured')

    tenant_uuid = app.config['auth'].get('master_tenant_uuid')
    if not tenant_uuid:
        raise MasterTenantNotInitialized()
    return tenant_uuid


master_tenant_uuid = Proxy(get_master_tenant_uuid)
