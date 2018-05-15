# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

from .base_dird_phoned_integration_test import BaseDirdPhonedIntegrationTest
from .base_dird_phoned_integration_test import DEFAULT_PROFILE
from .base_dird_phoned_integration_test import VALID_TERM
from .base_dird_phoned_integration_test import VALID_VENDOR
from .base_dird_phoned_integration_test import VALID_XIVO_USER_UUID

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import contains_string


class TestHTTPSMissingCertificate(BaseDirdPhonedIntegrationTest):
    asset = 'no_ssl_certificate'

    def test_given_inexisting_SSL_certificate_when_dird_phoned_starts_then_dird_phoned_https_stop(self):
        log = self.service_logs('phoned')
        assert_that(log, contains_string("HTTPS server won't start"))

    def test_given_inexisting_SSL_certificate_when_dird_phoned_starts_then_dird_phoned_http_start(self):
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE,
                                          term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))


class TestHTTPSMissingPrivateKey(BaseDirdPhonedIntegrationTest):
    asset = 'no_ssl_private_key'

    def test_given_inexisting_SSL_private_key_when_dird_phoned_starts_then_dird_phoned_http_start(self):
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE,
                                          term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))

    def test_given_inexisting_SSL_private_key_when_dird_phoned_starts_then_dird_phoned_https_stop(self):
        log = self.service_logs('phoned')
        assert_that(log, contains_string("HTTPS server won't start"))
