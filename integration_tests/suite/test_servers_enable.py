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

import time

from .base_dird_phoned_integration_test import BaseDirdPhonedIntegrationTest
from .base_dird_phoned_integration_test import DEFAULT_PROFILE
from .base_dird_phoned_integration_test import VALID_TERM
from .base_dird_phoned_integration_test import VALID_VENDOR
from .base_dird_phoned_integration_test import VALID_XIVO_USER_UUID

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import contains_string


class TestHTTPSIsDisabled(BaseDirdPhonedIntegrationTest):
    asset = 'https_enable_false'

    def test_configuration_https_enable_false_when_dird_phoned_starts_then_dird_phoned_https_stop(self):
        log = self.service_logs('phoned')
        assert_that(log, contains_string('HTTPS server is disabled'))

    def test_configuration_https_enable_false_when_dird_phoned_starts_then_dird_phoned_http_start(self):
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE,
                                          term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))


class TestHTTPIsDisabled(BaseDirdPhonedIntegrationTest):
    asset = 'http_enable_false'

    def test_configuration_http_enable_false_when_dird_phoned_starts_then_dird_phoned_http_stop(self):
        log = self.service_logs('phoned')
        assert_that(log, contains_string('HTTP server is disabled'))

    def test_configuration_http_enable_false_when_dird_phoned_starts_then_dird_phoned_https_start(self):
        response = self.get_ssl_lookup_result(vendor=VALID_VENDOR,
                                              xivo_user_uuid=VALID_XIVO_USER_UUID,
                                              profile=DEFAULT_PROFILE,
                                              term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))


class TestHTTPandHTTPSAreDisabled(BaseDirdPhonedIntegrationTest):
    asset = 'http_and_https_enable_false'

    def test_configuration_http_and_https_enable_false_when_dird_phoned_starts_then_dird_phoned_stop(self):
        for _ in range(2):
            status = self.service_status('phoned')
            if not status['State']['Running']:
                break
            time.sleep(1)
        else:
            self.fail('xivo-dird-phoned did not stop while http and https server are disabled')

        log = self.service_logs('phoned')
        assert_that(log, contains_string('No HTTP/HTTPS server enabled'))
