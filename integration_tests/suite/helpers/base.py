# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os

import requests

from xivo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase

from xivo_test_helpers.wait_strategy import NoWaitStrategy

logger = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()

ASSETS_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
CA_CERT = os.path.join(ASSETS_ROOT, 'ssl', 'server.crt')

DEFAULT_PROFILE = 'default_phone'
VALID_TERM = 'toto'
VALID_VENDOR = 'cisco'
VALID_XIVO_USER_UUID = '00000000-0000-0000-0000-000000000001'


class BaseDirdPhonedIntegrationTest(AssetLaunchingTestCase):

    assets_root = ASSETS_ROOT
    service = 'phoned'
    wait_strategy = NoWaitStrategy()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wait_strategy.wait(cls)

    @classmethod
    def get_status_result(self):
        url = u'http://localhost:{port}/0.1/status'
        port = self.service_port(9498, 'phoned')
        result = requests.get(url.format(port=port))
        return result

    @classmethod
    def get_status_result_by_https(self):
        url = u'https://localhost:{port}/0.1/status'
        port = self.service_port(9499, 'phoned')
        result = requests.get(url.format(port=port), verify=False)
        return result

    @classmethod
    def get_menu_result(self, profile, vendor, xivo_user_uuid=None):
        url = 'http://localhost:{port}/0.1/directories/menu/{profile}/{vendor}'
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9498, 'phoned')
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params)
        return result

    @classmethod
    def get_ssl_menu_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/menu/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params, verify=False)
        return result

    @classmethod
    def get_menu_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/menu/autodetect'.format(port=port)
        result = requests.get(url, headers=headers)
        return result

    @classmethod
    def get_ssl_menu_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/menu/autodetect'.format(port=port)
        result = requests.get(url, headers=headers, verify=False)
        return result

    @classmethod
    def get_input_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/input/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params)
        return result

    @classmethod
    def get_ssl_input_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/input/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params, verify=False)
        return result

    @classmethod
    def get_input_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/input/autodetect'.format(port=port)
        result = requests.get(url, headers=headers)
        return result

    @classmethod
    def get_ssl_input_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/input/autodetect'.format(port=port)
        result = requests.get(url, headers=headers, verify=False)
        return result

    @classmethod
    def get_lookup_result(self, profile, vendor, xivo_user_uuid=None, term=None, headers=None):
        params = {'xivo_user_uuid': xivo_user_uuid, 'term': term}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/lookup/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params, headers=headers)
        return result

    @classmethod
    def get_lookup_gigaset_result(self, profile, xivo_user_uuid=None, term=None, headers=None):
        params = {'term': term}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/lookup/{profile}/gigaset/{xivo_user_uuid}'
        result = requests.get(url.format(port=port, profile=profile, xivo_user_uuid=xivo_user_uuid), params=params, headers=headers)
        return result

    @classmethod
    def get_lookup_autodetect_result(self, term=None, user_agent=None):
        params = {'term': term}
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/lookup/autodetect'.format(port=port)
        result = requests.get(url, params=params, headers=headers)
        return result

    @classmethod
    def get_ssl_lookup_result(self, profile, vendor, xivo_user_uuid=None, term=None):
        params = {'xivo_user_uuid': xivo_user_uuid, 'term': term}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/lookup/{profile}/{vendor}'
        result = requests.get(url.format(port=port, profile=profile, vendor=vendor), params=params, verify=False)
        return result

    @classmethod
    def get_ssl_lookup_gigaset_result(self, profile, xivo_user_uuid=None, term=None):
        params = {'term': term}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/lookup/{profile}/gigaset/{xivo_user_uuid}'
        result = requests.get(url.format(port=port, profile=profile, xivo_user_uuid=xivo_user_uuid), params=params, verify=False)
        return result

    @classmethod
    def get_ssl_lookup_autodetect_result(self, term=None, user_agent=None):
        params = {'term': term}
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/lookup/autodetect'.format(port=port)
        result = requests.get(url, params=params, headers=headers, verify=False)
        return result
