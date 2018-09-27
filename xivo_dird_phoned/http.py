# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging
import requests

from flask import request
from flask import Response
from flask import current_app
from flask_restful import reqparse
from requests.exceptions import RequestException
from time import time
from xivo_dird_phoned.rest_api import api
from xivo_dird_phoned.auth_remote_addr import AuthResource

logger = logging.getLogger(__name__)

parser = reqparse.RequestParser()
parser.add_argument('xivo_user_uuid', type=str, required=True, location='args')

parser_lookup = parser.copy()
parser_lookup.add_argument('limit', type=int, required=False, help='limit cannot be converted', location='args')
parser_lookup.add_argument('offset', type=int, required=False, help='offset cannot be converted', location='args')
parser_lookup.add_argument('term', type=str, required=True, help='term is missing', location='args')

parser_lookup_gigaset = reqparse.RequestParser()
parser_lookup_gigaset.add_argument('first', type=int, default=1, help='first cannot be converted', location='args')
parser_lookup_gigaset.add_argument('count', type=int, dest='limit', required=False, help='count cannot be converted', location='args')
parser_lookup_gigaset.add_argument('set_first', dest='term', default='', required=False, location='args')

parser_lookup_autodetect = parser_lookup.copy()
parser_lookup_autodetect.remove_argument('xivo_user_uuid')

DIRD_API_VERSION = '0.1'
FAKE_XIVO_USER_UUID = '00000000-0000-0000-0000-000000000000'


class XivoAuthConnectionError(RequestException):

    code = 503

    def __str__(self):
        return 'Connection to XiVO Auth failed'


class XivoDirdConnectionError(RequestException):

    code = 503

    def __str__(self):
        return 'Connection to XiVO Dird failed'


def _error(code, msg):
    return {'reason': [msg],
            'timestamp': [time()],
            'status_code': code}, code


class DirectoriesConfiguration:

    status_url = '/status'
    menu_url = '/directories/menu/<profile>/<vendor>'
    input_url = '/directories/input/<profile>/<vendor>'
    lookup_url = '/directories/lookup/<profile>/<vendor>'
    lookup_gigaset_url = '/directories/lookup/<profile>/gigaset/<xivo_user_uuid>'
    menu_autodetect_url = '/directories/menu/autodetect'
    input_autodetect_url = '/directories/input/autodetect'
    lookup_autodetect_url = '/directories/lookup/autodetect'

    def __init__(self, dird_config):
        dird_host = dird_config['host']
        dird_port = dird_config['port']
        dird_default_profile = dird_config['default_profile']
        dird_verify_certificate = dird_config.get('verify_certificate', True)

        api.add_resource(Status, self.status_url)

        Menu.configure(dird_host, dird_port, dird_verify_certificate)
        Input.configure(dird_host, dird_port, dird_verify_certificate)
        Lookup.configure(dird_host, dird_port, dird_verify_certificate)
        LookupGigaset.configure(dird_host, dird_port, dird_verify_certificate)
        api.add_resource(Menu, self.menu_url)
        api.add_resource(Input, self.input_url)
        api.add_resource(Lookup, self.lookup_url)
        api.add_resource(LookupGigaset, self.lookup_gigaset_url)

        MenuAutodetect.configure(dird_host, dird_port, dird_verify_certificate, dird_default_profile)
        InputAutodetect.configure(dird_host, dird_port, dird_verify_certificate, dird_default_profile)
        LookupAutodetect.configure(dird_host, dird_port, dird_verify_certificate, dird_default_profile)
        api.add_resource(MenuAutodetect, self.menu_autodetect_url)
        api.add_resource(InputAutodetect, self.input_autodetect_url)
        api.add_resource(LookupAutodetect, self.lookup_autodetect_url)


class Status(AuthResource):

    def get(self):
        return {'service_token': 'ok' if current_app.config.get('token') else 'fail'}


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
        args = parser.parse_args()
        xivo_user_uuid = args['xivo_user_uuid']
        url = 'https://{host}:{port}/{version}/directories/menu/{profile}/{xivo_user_uuid}/{vendor}'

        try:
            headers = {'X-Auth-Token': current_app.config.get('token'),
                       'Proxy-URL': _build_next_url('menu'),
                       'Accept-Language': request.headers.get('Accept-Language')}
            headers.update(request.headers)
            return _response_dird(url.format(host=self.dird_host,
                                             port=self.dird_port,
                                             version=DIRD_API_VERSION,
                                             profile=profile,
                                             xivo_user_uuid=xivo_user_uuid,
                                             vendor=vendor),
                                  headers=headers,
                                  verify=self.dird_verify_certificate)
        except RequestException as e:
            return _error(e.code, str(e))


# XXX Migration code
class MenuAutodetect(AuthResource):

    dird_default_profile = None
    dird_host = None
    dird_port = None
    dird_verify_certificate = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_certificate, dird_default_profile):
        cls.dird_default_profile = dird_default_profile
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_certificate = dird_verify_certificate

    def get(self):
        xivo_user_uuid = FAKE_XIVO_USER_UUID
        profile = self.dird_default_profile
        url = 'https://{host}:{port}/{version}/directories/menu/{profile}/{xivo_user_uuid}/{vendor}'

        vendor = _find_vendor_by_user_agent(request.headers.get('User-Agent', ''))
        if not vendor:
            return _error(404, 'No vendor found')

        try:
            headers = {'X-Auth-Token': current_app.config.get('token'),
                       'Proxy-URL': _build_next_url('menu'),
                       'Accept-Language': request.headers.get('Accept-Language')}
            return _response_dird(url.format(host=self.dird_host,
                                             port=self.dird_port,
                                             version=DIRD_API_VERSION,
                                             profile=profile,
                                             xivo_user_uuid=xivo_user_uuid,
                                             vendor=vendor),
                                  headers=headers,
                                  verify=self.dird_verify_certificate)
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
        args = parser.parse_args()
        xivo_user_uuid = args['xivo_user_uuid']
        url = 'https://{host}:{port}/{version}/directories/input/{profile}/{xivo_user_uuid}/{vendor}'

        try:
            headers = {'X-Auth-Token': current_app.config.get('token'),
                       'Proxy-URL': _build_next_url('input'),
                       'Accept-Language': request.headers.get('Accept-Language')}
            return _response_dird(url.format(host=self.dird_host,
                                             port=self.dird_port,
                                             version=DIRD_API_VERSION,
                                             profile=profile,
                                             xivo_user_uuid=xivo_user_uuid,
                                             vendor=vendor),
                                  headers=headers,
                                  verify=self.dird_verify_certificate)
        except RequestException as e:
            return _error(e.code, str(e))


class InputAutodetect(AuthResource):

    dird_default_profile = None
    dird_host = None
    dird_port = None
    dird_verify_certificate = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_certificate, dird_default_profile):
        cls.dird_default_profile = dird_default_profile
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_certificate = dird_verify_certificate

    def get(self):
        xivo_user_uuid = FAKE_XIVO_USER_UUID
        profile = self.dird_default_profile
        url = 'https://{host}:{port}/{version}/directories/input/{profile}/{xivo_user_uuid}/{vendor}'

        vendor = _find_vendor_by_user_agent(request.headers.get('User-Agent', ''))
        if not vendor:
            return _error(404, 'No vendor found')

        try:
            headers = {'X-Auth-Token': current_app.config.get('token'),
                       'Proxy-URL': _build_next_url('input'),
                       'Accept-Language': request.headers.get('Accept-Language')}
            return _response_dird(url.format(host=self.dird_host,
                                             port=self.dird_port,
                                             version=DIRD_API_VERSION,
                                             profile=profile,
                                             xivo_user_uuid=xivo_user_uuid,
                                             vendor=vendor),
                                  headers=headers,
                                  verify=self.dird_verify_certificate)
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
        args = parser_lookup.parse_args()
        limit = args['limit']
        offset = args['offset']
        term = args['term']
        xivo_user_uuid = args['xivo_user_uuid']

        url = 'https://{host}:{port}/{version}/directories/lookup/{profile}/{xivo_user_uuid}/{vendor}'
        params = {'term': term, 'limit': limit, 'offset': offset}

        try:
            headers = {'X-Auth-Token': current_app.config.get('token'),
                       'Proxy-URL': _build_next_url('lookup'),
                       'Accept-Language': request.headers.get('Accept-Language')}
            return _response_dird(url.format(host=self.dird_host,
                                             port=self.dird_port,
                                             version=DIRD_API_VERSION,
                                             profile=profile,
                                             xivo_user_uuid=xivo_user_uuid,
                                             vendor=vendor),
                                  headers=headers,
                                  params=params,
                                  verify=self.dird_verify_certificate)
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
        args = parser_lookup_gigaset.parse_args()
        offset = args['first'] - 1
        limit = args['limit']
        term = args['term'].replace('*', '') if args['term'] else ''

        url = 'https://{host}:{port}/{version}/directories/lookup/{profile}/{xivo_user_uuid}/gigaset'
        params = {'term': term, 'limit': limit, 'offset': offset}

        try:
            headers = {'X-Auth-Token': current_app.config.get('token'),
                       'Proxy-URL': _build_next_url('lookup'),
                       'Accept-Language': request.headers.get('Accept-Language')}
            return _response_dird(url.format(host=self.dird_host,
                                             port=self.dird_port,
                                             version=DIRD_API_VERSION,
                                             profile=profile,
                                             xivo_user_uuid=xivo_user_uuid),
                                  headers=headers,
                                  params=params,
                                  verify=self.dird_verify_certificate)
        except RequestException as e:
            return _error(e.code, str(e))


class LookupAutodetect(AuthResource):

    dird_default_profile = None
    dird_host = None
    dird_port = None
    dird_verify_certificate = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_certificate, dird_default_profile):
        cls.dird_default_profile = dird_default_profile
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_certificate = dird_verify_certificate

    def get(self):
        args = parser_lookup_autodetect.parse_args()
        limit = args['limit']
        offset = args['offset']
        term = args['term']
        xivo_user_uuid = FAKE_XIVO_USER_UUID
        profile = self.dird_default_profile
        url = 'https://{host}:{port}/{version}/directories/lookup/{profile}/{xivo_user_uuid}/{vendor}'
        params = {'term': term, 'limit': limit, 'offset': offset}

        vendor = _find_vendor_by_user_agent(request.headers.get('User-Agent', ''))
        if not vendor:
            return _error(404, 'No vendor found')

        try:
            headers = {'X-Auth-Token': current_app.config.get('token'),
                       'Proxy-URL': _build_next_url('lookup'),
                       'Accept-Language': request.headers.get('Accept-Language')}
            return _response_dird(url.format(host=self.dird_host,
                                             port=self.dird_port,
                                             version=DIRD_API_VERSION,
                                             profile=profile,
                                             xivo_user_uuid=xivo_user_uuid,
                                             vendor=vendor),
                                  headers=headers,
                                  params=params,
                                  verify=self.dird_verify_certificate)
        except RequestException as e:
            return _error(e.code, str(e))


def _find_vendor_by_user_agent(raw_user_agent):
    user_agent = raw_user_agent.lower()

    if 'aastra' in user_agent:
        # '/^Aastra((?:(?:67)?5[1357]|673[01])i(?: CT)?) /'
        return 'aastra'
    elif 'cisco' in user_agent or 'allegro' in user_agent:
        # '/Allegro-/i'
        return 'cisco'
    elif 'polycom' in user_agent:
        return 'polycom'
    elif 'snom' in user_agent:
        # '/(snom3[026]0)-/'
        return 'snom'
    elif 'thomson' in user_agent:
        # '/^THOMSON (ST2022|ST2030|TB30) /'
        return 'thomson'
    elif 'yealink' in user_agent:
        return 'yealink'
    return None


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
        raise XivoDirdConnectionError()
    if r.status_code == 401:
        raise XivoAuthConnectionError()

    return Response(response=r.content, content_type=r.headers['content-type'], status=r.status_code)
