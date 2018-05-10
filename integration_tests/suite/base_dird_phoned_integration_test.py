# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

import requests
import os
import logging

from xivo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase

logger = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()

ASSETS_ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets')
CA_CERT = os.path.join(ASSETS_ROOT, '_common', 'ssl', 'server.crt')

DEFAULT_PROFILE = 'default_phone'
VALID_TERM = 'toto'
VALID_USER_AGENT = 'Allegro-Software-WebClient/4.34'
VALID_VENDOR = 'cisco'
VALID_XIVO_USER_UUID = '00000000-0000-0000-0000-000000000001'


class BaseDirdPhonedIntegrationTest(AssetLaunchingTestCase):

    assets_root = ASSETS_ROOT
    service = 'phoned'

    @classmethod
    def get_menu_result(self, profile, vendor, xivo_user_uuid=None):
        url = u'http://localhost:{port}/0.1/directories/menu/{profile}/{vendor}'
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9498, 'phoned')
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params)
        return result

    @classmethod
    def get_ssl_menu_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9499, 'phoned')
        url = u'https://localhost:{port}/0.1/directories/menu/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params, verify=False)
        return result

    @classmethod
    def get_menu_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = u'http://localhost:{port}/0.1/directories/menu/autodetect'.format(port=port)
        result = requests.get(url, headers=headers)
        return result

    @classmethod
    def get_ssl_menu_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = u'https://localhost:{port}/0.1/directories/menu/autodetect'.format(port=port)
        result = requests.get(url, headers=headers, verify=False)
        return result

    @classmethod
    def get_input_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9498, 'phoned')
        url = u'http://localhost:{port}/0.1/directories/input/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params)
        return result

    @classmethod
    def get_ssl_input_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9499, 'phoned')
        url = u'https://localhost:{port}/0.1/directories/input/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params, verify=False)
        return result

    @classmethod
    def get_input_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = u'http://localhost:{port}/0.1/directories/input/autodetect'.format(port=port)
        result = requests.get(url, headers=headers)
        return result

    @classmethod
    def get_ssl_input_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = u'https://localhost:{port}/0.1/directories/input/autodetect'.format(port=port)
        result = requests.get(url, headers=headers, verify=False)
        return result

    @classmethod
    def get_lookup_result(self, profile, vendor, xivo_user_uuid=None, term=None, headers=None):
        params = {'xivo_user_uuid': xivo_user_uuid, 'term': term}
        port = self.service_port(9498, 'phoned')
        url = u'http://localhost:{port}/0.1/directories/lookup/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params, headers=headers)
        return result

    @classmethod
    def get_lookup_autodetect_result(self, term=None, user_agent=None):
        params = {'term': term}
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = u'http://localhost:{port}/0.1/directories/lookup/autodetect'.format(port=port)
        result = requests.get(url, params=params, headers=headers)
        return result

    @classmethod
    def get_ssl_lookup_result(self, profile, vendor, xivo_user_uuid=None, term=None):
        params = {'xivo_user_uuid': xivo_user_uuid, 'term': term}
        port = self.service_port(9499, 'phoned')
        url = u'https://localhost:{port}/0.1/directories/lookup/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params, verify=False)
        return result

    @classmethod
    def get_ssl_lookup_autodetect_result(self, term=None, user_agent=None):
        params = {'term': term}
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = u'https://localhost:{port}/0.1/directories/lookup/autodetect'.format(port=port)
        result = requests.get(url, params=params, headers=headers, verify=False)
        return result
