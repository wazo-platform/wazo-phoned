# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import requests
import yaml

from openapi_spec_validator import validate_v2_spec

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
        api_url = 'https://localhost:{port}/{version}/api/api.yml'.format(port=port, version=VERSION)
        api = requests.get(api_url, verify=False)
        validate_v2_spec(yaml.safe_load(api.text))
