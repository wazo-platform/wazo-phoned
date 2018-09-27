# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
)

from xivo_test_helpers import until
from .base_dird_phoned_integration_test import (
    BaseDirdPhonedIntegrationTest,
    DEFAULT_PROFILE,
    VALID_TERM,
    VALID_USER_AGENT,
    VALID_VENDOR,
    VALID_XIVO_USER_UUID,
)


class TestStatusCodeDirdPhoned(BaseDirdPhonedIntegrationTest):

    asset = 'default_config'

    @classmethod
    def setUpClass(self):
        super(TestStatusCodeDirdPhoned, self).setUpClass()

        def phoned_is_ready():
            status = self.get_status_result().json()
            assert_that(status, has_entries(service_token='ok'))

        until.assert_(phoned_is_ready, tries=60)

    # Menu
    def test_that_menu_return_no_error_when_query_ssl(self):
        response = self.get_ssl_menu_result(vendor=VALID_VENDOR,
                                            xivo_user_uuid=VALID_XIVO_USER_UUID,
                                            profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(200))

    def test_that_menu_return_no_error_when_query(self):
        response = self.get_menu_result(vendor=VALID_VENDOR,
                                        xivo_user_uuid=VALID_XIVO_USER_UUID,
                                        profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(200))

    def test_that_menu_return_error_when_no_xivo_user_uuid(self):
        response = self.get_menu_result(vendor=VALID_VENDOR,
                                        profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(400))

    # Input
    def test_that_input_return_no_error_when_query_ssl(self):
        response = self.get_ssl_input_result(vendor=VALID_VENDOR,
                                             xivo_user_uuid=VALID_XIVO_USER_UUID,
                                             profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(200))

    def test_that_input_return_no_error_when_query(self):
        response = self.get_input_result(vendor=VALID_VENDOR,
                                         xivo_user_uuid=VALID_XIVO_USER_UUID,
                                         profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(200))

    def test_that_input_return_error_when_no_xivo_user_uuid(self):
        response = self.get_input_result(vendor=VALID_VENDOR,
                                         profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(400))

    # Lookup
    def test_that_lookup_return_no_error_when_query_ssl(self):
        response = self.get_ssl_lookup_result(vendor=VALID_VENDOR,
                                              xivo_user_uuid=VALID_XIVO_USER_UUID,
                                              profile=DEFAULT_PROFILE,
                                              term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_return_no_error_when_query(self):
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE,
                                          term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_return_error_when_no_xivo_user_uuid(self):
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          profile=DEFAULT_PROFILE,
                                          term=VALID_TERM)

        assert_that(response.status_code, equal_to(400))

    def test_that_lookup_return_error_when_no_term(self):
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(400))

    # Lookup Gigaset
    def test_that_lookup_gigaset_return_no_error_when_query_ssl(self):
        response = self.get_ssl_lookup_gigaset_result(xivo_user_uuid=VALID_XIVO_USER_UUID,
                                                      profile=DEFAULT_PROFILE,
                                                      term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_gigaset_return_no_error_when_query(self):
        response = self.get_lookup_gigaset_result(xivo_user_uuid=VALID_XIVO_USER_UUID,
                                                  profile=DEFAULT_PROFILE,
                                                  term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_gigaset_return_no_error_when_no_term(self):
        response = self.get_lookup_gigaset_result(xivo_user_uuid=VALID_XIVO_USER_UUID,
                                                  profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(200))

    # Menu autodetect
    def test_that_menu_autodetect_return_no_error_when_query_ssl(self):
        response = self.get_ssl_menu_autodetect_result(user_agent=VALID_USER_AGENT)

        assert_that(response.status_code, equal_to(200))

    def test_that_menu_autodetect_return_no_error_when_query(self):
        response = self.get_menu_autodetect_result(user_agent=VALID_USER_AGENT)

        assert_that(response.status_code, equal_to(200))

    def test_that_menu_autodetect_return_error_when_no_user_agent(self):
        response = self.get_menu_autodetect_result()

        assert_that(response.status_code, equal_to(404))

    # Input autodetect
    def test_that_input_autodetect_return_no_error_when_query_ssl(self):
        response = self.get_ssl_input_autodetect_result(user_agent=VALID_USER_AGENT)

        assert_that(response.status_code, equal_to(200))

    def test_that_input_autodetect_return_no_error_when_query(self):
        response = self.get_input_autodetect_result(user_agent=VALID_USER_AGENT)

        assert_that(response.status_code, equal_to(200))

    def test_that_input_autodetect_return_error_when_no_user_agent(self):
        response = self.get_input_autodetect_result()

        assert_that(response.status_code, equal_to(404))

    # Lookup autodetect
    def test_that_lookup_autodetect_return_no_error_when_query_ssl(self):
        response = self.get_ssl_lookup_autodetect_result(user_agent=VALID_USER_AGENT,
                                                         term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_autodetect_return_no_error_when_query(self):
        response = self.get_lookup_autodetect_result(user_agent=VALID_USER_AGENT,
                                                     term=VALID_TERM)

        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_autodetect_return_error_when_no_user_agent(self):
        response = self.get_lookup_autodetect_result(term=VALID_TERM)

        assert_that(response.status_code, equal_to(404))

    def test_that_lookup_autodetect_return_error_when_no_term(self):
        response = self.get_lookup_autodetect_result(user_agent=VALID_USER_AGENT)

        assert_that(response.status_code, equal_to(400))


class TestAuthError(BaseDirdPhonedIntegrationTest):

    asset = 'no_auth_server'

    def test_no_auth_server_gives_503(self):
        response = self.get_menu_result(vendor=VALID_VENDOR,
                                        xivo_user_uuid=VALID_XIVO_USER_UUID,
                                        profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(503))


class TestDirdError(BaseDirdPhonedIntegrationTest):

    asset = 'no_dird_server'

    def test_no_dird_server_gives_503(self):
        response = self.get_menu_result(vendor=VALID_VENDOR,
                                        xivo_user_uuid=VALID_XIVO_USER_UUID,
                                        profile=DEFAULT_PROFILE)

        assert_that(response.status_code, equal_to(503))
