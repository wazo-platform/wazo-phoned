# -*- coding: utf-8 -*-

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

import subprocess
import requests
import os
import json
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

    @classmethod
    def dird_phoned_status(cls):
        dird_phoned_id = cls._run_cmd('docker-compose ps -q phoned').strip()
        status = cls._run_cmd('docker inspect {container}'.format(container=dird_phoned_id))
        return json.loads(status)

    @classmethod
    def dird_phoned_logs(cls):
        return cls.service_logs('phoned')

    @staticmethod
    def _run_cmd(cmd):
        process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = process.communicate()
        logger.info(out)
        return out

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
