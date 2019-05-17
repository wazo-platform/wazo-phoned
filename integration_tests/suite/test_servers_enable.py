# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from hamcrest import (
    assert_that,
    contains_string,
    equal_to,
)

from .helpers.base import (
    BaseDirdPhonedIntegrationTest,
    DEFAULT_PROFILE,
    VALID_TERM,
    VALID_VENDOR,
    VALID_XIVO_USER_UUID,
)
from .helpers.wait_strategy import DirdPhonedEverythingUpWaitStrategy


class TestHTTPSIsDisabled(BaseDirdPhonedIntegrationTest):
    asset = 'https_enable_false'

    def test_configuration_https_enable_false_when_dird_phoned_starts_then_dird_phoned_https_stop(self):
        log = self.service_logs('phoned')
        assert_that(log, contains_string('HTTPS server is disabled'))

    def test_configuration_https_enable_false_when_dird_phoned_starts_then_dird_phoned_http_start(self):
        response = self.get_lookup_result(
            vendor=VALID_VENDOR,
            xivo_user_uuid=VALID_XIVO_USER_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))


class TestHTTPIsDisabled(BaseDirdPhonedIntegrationTest):
    asset = 'http_enable_false'
    wait_strategy = DirdPhonedEverythingUpWaitStrategy()

    def test_configuration_http_enable_false_when_dird_phoned_starts_then_dird_phoned_http_stop(self):
        log = self.service_logs('phoned')
        assert_that(log, contains_string('HTTP server is disabled'))

    def test_configuration_http_enable_false_when_dird_phoned_starts_then_dird_phoned_https_start(self):
        response = self.get_ssl_lookup_result(
            vendor=VALID_VENDOR,
            xivo_user_uuid=VALID_XIVO_USER_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
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
            self.fail('wazo-dird-phoned did not stop while http and https server are disabled')

        log = self.service_logs('phoned')
        assert_that(log, contains_string('No HTTP/HTTPS server enabled'))
