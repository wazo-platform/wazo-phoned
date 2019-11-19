# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os

import requests

from wazo_auth_client import Client as AuthClient
from xivo.config_helper import parse_config_file
from xivo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase
from xivo_test_helpers.auth import (
    AuthClient as MockAuthClient,
    MockCredentials,
    MockUserToken,
)
from xivo_test_helpers.wait_strategy import NoWaitStrategy

logger = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()

ASSETS_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
CA_CERT = os.path.join(ASSETS_ROOT, 'ssl', 'server.crt')

DEFAULT_PROFILE = 'default_phone'
VALID_TERM = 'toto'
VALID_VENDOR = 'cisco'

VALID_TOKEN = 'valid-token'

WAZO_UUID = 'de8f8614-9f42-4fb6-be5a-f9a8d4f8674b'

MASTER_TOKEN = '8843a6b5-75e9-4472-8c8c-4a5c605bd47c'
MASTER_USER_UUID = '5f243438-a429-46a8-a992-baed872081e0'
MASTER_TENANT = '16d4c16b-eb84-4a09-a3a9-c8cfdf67c8f1'

USERS_TENANT = '938bb555-812d-48c7-9dcb-81f30bd99679'
USER_1_UUID = 'f2ad2e07-11df-4986-9ecc-c9a29a349725'
USER_1_TOKEN = '0d74df1c-e59c-4c7a-9f4f-db8ea1f6cd94'


class BasePhonedIntegrationTest(AssetLaunchingTestCase):

    assets_root = ASSETS_ROOT
    service = 'phoned'
    wait_strategy = NoWaitStrategy()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wait_strategy.wait(cls)
        if cls.asset != 'no_auth_server':
            cls.configure_wazo_auth()

    @classmethod
    def make_auth(cls):
        return AuthClient(
            'localhost', cls.service_port(9497, 'auth'), verify_certificate=False
        )

    @classmethod
    def make_mock_auth(cls):
        return MockAuthClient('localhost', cls.service_port(9497, 'auth'))

    @classmethod
    def configure_wazo_auth(cls):
        key_file = parse_config_file(
            os.path.join(cls.assets_root, 'auth_keys', 'wazo-phoned-key.yml')
        )
        mock_auth = cls.make_mock_auth()
        mock_auth.set_valid_credentials(
            MockCredentials(key_file['service_id'], key_file['service_key']),
            MASTER_TOKEN,
        )
        mock_auth.set_token(
            MockUserToken(
                MASTER_TOKEN,
                MASTER_USER_UUID,
                WAZO_UUID,
                {'tenant_uuid': MASTER_TENANT, 'uuid': MASTER_USER_UUID},
            )
        )
        mock_auth.set_token(
            MockUserToken(
                USER_1_TOKEN,
                USER_1_UUID,
                WAZO_UUID,
                {'tenant_uuid': USERS_TENANT, 'uuid': USER_1_UUID},
            )
        )

        mock_auth.set_tenants(
            {
                'uuid': MASTER_TENANT,
                'name': 'phoned-tests-master',
                'parent_uuid': MASTER_TENANT,
            },
            {
                'uuid': USERS_TENANT,
                'name': 'phoned-tests-users',
                'parent_uuid': MASTER_TENANT,
            },
        )

        auth = cls.make_auth()
        auth.users.new(
            uuid=USER_1_UUID, tenant_uuid=USERS_TENANT,
        )

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
        result = requests.get(
            url.format(port=port, profile=profile, vendor=vendor), params=params
        )
        return result

    @classmethod
    def get_ssl_menu_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/menu/{profile}/{vendor}'
        result = requests.get(
            url.format(port=port, profile=profile, vendor=vendor),
            params=params,
            verify=False,
        )
        return result

    @classmethod
    def get_menu_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/menu/autodetect'.format(
            port=port
        )
        result = requests.get(url, headers=headers)
        return result

    @classmethod
    def get_ssl_menu_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/menu/autodetect'.format(
            port=port
        )
        result = requests.get(url, headers=headers, verify=False)
        return result

    @classmethod
    def get_input_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/input/{profile}/{vendor}'
        result = requests.get(
            url.format(port=port, profile=profile, vendor=vendor), params=params
        )
        return result

    @classmethod
    def get_ssl_input_result(self, profile, vendor, xivo_user_uuid=None):
        params = {'xivo_user_uuid': xivo_user_uuid}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/input/{profile}/{vendor}'
        result = requests.get(
            url.format(port=port, profile=profile, vendor=vendor),
            params=params,
            verify=False,
        )
        return result

    @classmethod
    def get_input_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/input/autodetect'.format(
            port=port
        )
        result = requests.get(url, headers=headers)
        return result

    @classmethod
    def get_ssl_input_autodetect_result(self, user_agent=None):
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/input/autodetect'.format(
            port=port
        )
        result = requests.get(url, headers=headers, verify=False)
        return result

    @classmethod
    def get_lookup_result(
        self, profile, vendor, xivo_user_uuid=None, term=None, headers=None
    ):
        params = {'xivo_user_uuid': xivo_user_uuid, 'term': term}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/lookup/{profile}/{vendor}'
        result = requests.get(
            url.format(port=port, profile=profile, vendor=vendor),
            params=params,
            headers=headers,
        )
        return result

    @classmethod
    def get_lookup_gigaset_result(
        self, profile, xivo_user_uuid=None, term=None, headers=None
    ):
        params = {'term': term}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/lookup/{profile}/gigaset/{xivo_user_uuid}'
        result = requests.get(
            url.format(port=port, profile=profile, xivo_user_uuid=xivo_user_uuid),
            params=params,
            headers=headers,
        )
        return result

    @classmethod
    def get_lookup_autodetect_result(self, term=None, user_agent=None):
        params = {'term': term}
        headers = {'User-Agent': user_agent}
        port = self.service_port(9498, 'phoned')
        url = 'http://localhost:{port}/0.1/directories/lookup/autodetect'.format(
            port=port
        )
        result = requests.get(url, params=params, headers=headers)
        return result

    @classmethod
    def get_ssl_lookup_result(
        self, profile, vendor, xivo_user_uuid=None, term=None, headers=None, **kwargs
    ):
        params = {'xivo_user_uuid': xivo_user_uuid, 'term': term}
        if kwargs:
            params.update(**kwargs)
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/lookup/{profile}/{vendor}'
        result = requests.get(
            url.format(port=port, profile=profile, vendor=vendor),
            params=params,
            headers=headers,
            verify=False,
        )
        return result

    @classmethod
    def get_ssl_lookup_gigaset_result(self, profile, xivo_user_uuid=None, term=None):
        params = {'term': term}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/lookup/{profile}/gigaset/{xivo_user_uuid}'
        result = requests.get(
            url.format(port=port, profile=profile, xivo_user_uuid=xivo_user_uuid),
            params=params,
            verify=False,
        )
        return result

    @classmethod
    def get_ssl_lookup_autodetect_result(self, term=None, user_agent=None):
        params = {'term': term}
        headers = {'User-Agent': user_agent}
        port = self.service_port(9499, 'phoned')
        url = 'https://localhost:{port}/0.1/directories/lookup/autodetect'.format(
            port=port
        )
        result = requests.get(url, params=params, headers=headers, verify=False)
        return result
