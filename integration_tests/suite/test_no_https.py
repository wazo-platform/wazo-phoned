# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import (
    assert_that,
    contains_string,
    equal_to,
)

from .base_dird_phoned_integration_test import (
    BaseDirdPhonedIntegrationTest,
    DEFAULT_PROFILE,
    VALID_TERM,
    VALID_VENDOR,
    VALID_XIVO_USER_UUID,
)


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
