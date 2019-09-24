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

from wazo_phoned.auth_remote_addr import AuthResource

from .exceptions import WazoAuthConnectionError, WazoDirdConnectionError
from .schema import UserUUIDSchema, LookupSchema, LookupGigasetSchema


DIRD_API_VERSION = '0.1'

logger = logging.getLogger(__name__)


def _error(code, msg):
    return {'reason': [msg], 'timestamp': [time()], 'status_code': code}, code


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
