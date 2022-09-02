# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import requests
import yaml

from openapi_spec_validator import validate_spec, openapi_v2_spec_validator

from .helpers.base import BasePhonedIntegrationTest
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger('openapi_spec_validator')
logger.setLevel(logging.INFO)

VERSION = '0.1'


class TestDocumentation(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_documentation_errors(self):
        port = self.service_port(9499, 'phoned')
        api_url = 'https://127.0.0.1:{port}/{version}/api/api.yml'.format(
            port=port, version=VERSION
        )
        api = requests.get(api_url, verify=False)
        validate_spec(yaml.safe_load(api.text), validator=openapi_v2_spec_validator)
