# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import requests

from flask import (
    request,
    Response,
    current_app,
)
from requests.exceptions import RequestException
from time import time

from xivo.mallow import fields
from xivo.mallow_helpers import Schema

from .auth_remote_addr import AuthResource
from .http_server import api

logger = logging.getLogger(__name__)

DIRD_API_VERSION = '0.1'


class UserUUIDSchema(Schema):
    xivo_user_uuid = fields.String(required=True)


class LookupSchema(UserUUIDSchema):
    term = fields.String(required=True)
    limit = fields.Integer(missing=None)
    offset = fields.Integer(missing=None)


class LookupGigasetSchema(Schema):
    set_first = fields.String(attribute='term', missing='')
    count = fields.Integer(attribute='limit', missing=None)
    first = fields.Integer(attribute='first', missing=1)


class WazoAuthConnectionError(RequestException):

    code = 503

    def __str__(self):
        return 'Connection to XiVO Auth failed'


class WazoDirdConnectionError(RequestException):

    code = 503

    def __str__(self):
        return 'Connection to XiVO Dird failed'


def _error(code, msg):
    return {'reason': [msg], 'timestamp': [time()], 'status_code': code}, code


class DirectoriesConfiguration:

    menu_url = '/directories/menu/<profile>/<vendor>'
    input_url = '/directories/input/<profile>/<vendor>'
    lookup_url = '/directories/lookup/<profile>/<vendor>'
    lookup_gigaset_url = '/directories/lookup/<profile>/gigaset/<xivo_user_uuid>'

    def __init__(self, dird_config):
        dird_host = dird_config['host']
        dird_port = dird_config['port']
        dird_verify_certificate = dird_config.get('verify_certificate', True)

        Menu.configure(dird_host, dird_port, dird_verify_certificate)
        Input.configure(dird_host, dird_port, dird_verify_certificate)
        Lookup.configure(dird_host, dird_port, dird_verify_certificate)
        LookupGigaset.configure(dird_host, dird_port, dird_verify_certificate)
        api.add_resource(Menu, self.menu_url)
        api.add_resource(Input, self.input_url)
        api.add_resource(Lookup, self.lookup_url)
        api.add_resource(LookupGigaset, self.lookup_gigaset_url)


class Menu(AuthResource):

    dird_host = None
    dird_port = None
    dird_verify_certificate = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_certificate):
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_certificate = dird_verify_certificate

    def get(self, profile, vendor):
        args = UserUUIDSchema().load(request.args)
        xivo_user_uuid = args['xivo_user_uuid']
        url = 'https://{host}:{port}/{version}/directories/menu/{profile}/{xivo_user_uuid}/{vendor}'

        try:
            headers = {
                'X-Auth-Token': current_app.config.get('token'),
                'Proxy-URL': _build_next_url('menu'),
                'Accept-Language': request.headers.get('Accept-Language'),
            }
            headers.update(request.headers)
            return _response_dird(
                url.format(
                    host=self.dird_host,
                    port=self.dird_port,
                    version=DIRD_API_VERSION,
                    profile=profile,
                    xivo_user_uuid=xivo_user_uuid,
                    vendor=vendor,
                ),
                headers=headers,
                verify=self.dird_verify_certificate,
            )
        except RequestException as e:
            return _error(e.code, str(e))


class Input(AuthResource):

    dird_host = None
    dird_port = None
    dird_verify_certificate = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_certificate):
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_certificate = dird_verify_certificate

    def get(self, profile, vendor):
        args = UserUUIDSchema().load(request.args)
        xivo_user_uuid = args['xivo_user_uuid']
        url = 'https://{host}:{port}/{version}/directories/input/{profile}/{xivo_user_uuid}/{vendor}'

        try:
            headers = {
                'X-Auth-Token': current_app.config.get('token'),
                'Proxy-URL': _build_next_url('input'),
                'Accept-Language': request.headers.get('Accept-Language'),
            }
            return _response_dird(
                url.format(
                    host=self.dird_host,
                    port=self.dird_port,
                    version=DIRD_API_VERSION,
                    profile=profile,
                    xivo_user_uuid=xivo_user_uuid,
                    vendor=vendor,
                ),
                headers=headers,
                verify=self.dird_verify_certificate,
            )
        except RequestException as e:
            return _error(e.code, str(e))


class Lookup(AuthResource):

    dird_host = None
    dird_port = None
    dird_verify_certificate = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_certificate):
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_certificate = dird_verify_certificate

    def get(self, profile, vendor):
        args = LookupSchema().load(request.args)
        limit = args['limit']
        offset = args['offset']
        term = args['term']
        xivo_user_uuid = args['xivo_user_uuid']

        url = 'https://{host}:{port}/{version}/directories/lookup/{profile}/{xivo_user_uuid}/{vendor}'
        params = {'term': term, 'limit': limit, 'offset': offset}

        try:
            headers = {
                'X-Auth-Token': current_app.config.get('token'),
                'Proxy-URL': _build_next_url('lookup'),
                'Accept-Language': request.headers.get('Accept-Language'),
            }
            return _response_dird(
                url.format(
                    host=self.dird_host,
                    port=self.dird_port,
                    version=DIRD_API_VERSION,
                    profile=profile,
                    xivo_user_uuid=xivo_user_uuid,
                    vendor=vendor,
                ),
                headers=headers,
                params=params,
                verify=self.dird_verify_certificate,
            )
        except RequestException as e:
            return _error(e.code, str(e))


class LookupGigaset(AuthResource):

    dird_host = None
    dird_port = None
    dird_verify_certificate = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_certificate):
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_certificate = dird_verify_certificate

    def get(self, profile, xivo_user_uuid):
        args = LookupGigasetSchema().load(request.args)
        offset = args['first'] - 1
        limit = args['limit']
        term = args['term'].replace('*', '') if args['term'] else ''

        url = 'https://{host}:{port}/{version}/directories/lookup/{profile}/{xivo_user_uuid}/gigaset'
        params = {'term': term, 'limit': limit, 'offset': offset}

        try:
            headers = {
                'X-Auth-Token': current_app.config.get('token'),
                'Proxy-URL': _build_next_url('lookup'),
                'Accept-Language': request.headers.get('Accept-Language'),
            }
            return _response_dird(
                url.format(
                    host=self.dird_host,
                    port=self.dird_port,
                    version=DIRD_API_VERSION,
                    profile=profile,
                    xivo_user_uuid=xivo_user_uuid,
                ),
                headers=headers,
                params=params,
                verify=self.dird_verify_certificate,
            )
        except RequestException as e:
            return _error(e.code, str(e))


def _build_next_url(current):
    if current == 'menu':
        return request.base_url.replace('menu', 'input', 1)
    if current == 'input':
        return request.base_url.replace('input', 'lookup', 1)
    if current == 'lookup':
        return request.base_url
    return None


def _response_dird(url, headers, verify, params=None):
    try:
        r = requests.get(url, headers=headers, verify=verify, params=params)
    except RequestException as e:
        logger.exception(e)
        raise WazoDirdConnectionError()
    if r.status_code == 401:
        raise WazoAuthConnectionError()

    return Response(response=r.content, content_type=r.headers['content-type'], status=r.status_code)
