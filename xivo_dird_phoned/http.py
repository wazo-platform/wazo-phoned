# -*- coding: utf-8 -*-
#
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

from flask import request
from flask import Response
from flask_restful import reqparse
from time import time
from xivo_dird_phoned.rest_api import api
from xivo_dird_phoned.auth_remote_addr import AuthResource
from xivo_dird_phoned import auth


logger = logging.getLogger(__name__)

AUTH_BACKEND = 'xivo_service'

parser = reqparse.RequestParser()
parser.add_argument('profile', type=unicode, required=False, location='args')
parser.add_argument('term', type=unicode, required=False, location='args')
parser.add_argument('vendor', type=unicode, required=False, location='args')
parser.add_argument('xivo_user_uuid', type=unicode, required=False, location='args')

# XXX Migration code
FAKE_XIVO_USER_UUID = '00000000-0000-0000-0000-000000000000'


def _error(code, msg):
    return {'reason': [msg],
            'timestamp': [time()],
            'status_code': code}, code


class DirectoriesConfiguration(object):

    menu_url = '/directories/menu'
    lookup_url = '/directories/lookup'

    def __init__(self, dird_config):
        dird_host = dird_config['host']
        dird_port = dird_config['port']
        dird_default_profile = dird_config['default_profile']
        dird_verify_cert = dird_config.get('verify_cert', True)
        LookupMenu.configure(dird_host, dird_port, dird_verify_cert, dird_default_profile)
        Lookup.configure(dird_host, dird_port, dird_verify_cert, dird_default_profile)
        api.add_resource(LookupMenu, self.menu_url)
        api.add_resource(Lookup, self.lookup_url)


class LookupMenu(AuthResource):

    dird_default_profile = None
    dird_host = None
    dird_port = None
    dird_verify_cert = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_cert, dird_default_profile):
        cls.dird_default_profile = dird_default_profile
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_cert = dird_verify_cert

    def get(self):
        args = parser.parse_args()
        profile = args['profile']
        vendor = args['vendor']
        xivo_user_uuid = args['xivo_user_uuid']

        # XXX Migration code
        if not vendor:
            user_agent = request.headers.get('User-agent', '').lower()
            vendor = find_vendor_by_user_agent(user_agent)
        # XXX Migration code
        if not xivo_user_uuid:
            xivo_user_uuid = FAKE_XIVO_USER_UUID
        # XXX Migration code
        if not profile:
            profile = self.dird_default_profile

        if not vendor:
            return _error(404, 'No vendor found')
        if not xivo_user_uuid:
            return _error(404, 'No xivo_user_uuid found')

        token_infos = auth.client().token.new(AUTH_BACKEND,
                                              expiration=10,
                                              backend_args={'xivo_user_uuid': xivo_user_uuid})

        headers = {'X-Auth-Token': token_infos['token'],
                   'Proxy-URL': request.base_url.replace('menu', 'lookup')}
        url = 'https://{host}:{port}{path}/{profile}/{vendor}'.format(host=self.dird_host,
                                                                      port=self.dird_port,
                                                                      path=request.path,
                                                                      profile=profile,
                                                                      vendor=vendor)
        r = requests.get(url, headers=headers, verify=self.dird_verify_cert)
        return Response(response=r.content,
                        content_type=r.headers['content-type'],
                        status=r.status_code)


class Lookup(AuthResource):

    dird_default_profile = None
    dird_host = None
    dird_port = None
    dird_verify_cert = None

    @classmethod
    def configure(cls, dird_host, dird_port, dird_verify_cert, dird_default_profile):
        cls.dird_default_profile = dird_default_profile
        cls.dird_host = dird_host
        cls.dird_port = dird_port
        cls.dird_verify_cert = dird_verify_cert

    def get(self):
        args = parser.parse_args()
        profile = args['profile']
        term = args['term']
        vendor = args['vendor']
        xivo_user_uuid = args['xivo_user_uuid']

        # XXX Migration code
        if not vendor:
            user_agent = request.headers.get('User-agent', '').lower()
            vendor = find_vendor_by_user_agent(user_agent)
        # XXX Migration code
        if not xivo_user_uuid:
            xivo_user_uuid = FAKE_XIVO_USER_UUID
        # XXX Migration code
        if not profile:
            profile = self.dird_default_profile

        if not vendor:
            return _error(404, 'No vendor found')
        if not xivo_user_uuid:
            return _error(404, 'No xivo_user_uuid found')

        token_infos = auth.client().token.new(AUTH_BACKEND,
                                              expiration=10,
                                              backend_args={'xivo_user_uuid': xivo_user_uuid})

        headers = {'X-Auth-Token': token_infos['token'],
                   'Proxy-URL': request.base_url}
        query = '?term={term}'.format(term=term) if term else ''
        url = 'https://{host}:{port}{path}/{profile}/{vendor}{query}'.format(host=self.dird_host,
                                                                             port=self.dird_port,
                                                                             path=request.path,
                                                                             profile=profile,
                                                                             vendor=vendor,
                                                                             query=query)
        r = requests.get(url, headers=headers, verify=self.dird_verify_cert)
        return Response(response=r.content,
                        content_type=r.headers['content-type'],
                        status=r.status_code)


# XXX Migration code
def find_vendor_by_user_agent(user_agent):

    if 'aastra' in user_agent:
        # '/^Aastra((?:(?:67)?5[1357]|673[01])i(?: CT)?) /'
        return 'aastra'
    elif 'cisco' in user_agent or 'allegro' in user_agent:
        # '/Allegro-/i'
        return 'cisco'
    elif 'snom' in user_agent:
        # '/(snom3[026]0)-/'
        return 'snom'
    elif 'thomson' in user_agent:
        # '/^THOMSON (ST2022|ST2030|TB30) /'
        return 'thomson'
    elif 'yealink' in user_agent:
        return 'yealink'
    return None
