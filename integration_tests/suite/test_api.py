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

from .base_dird_phoned_integration_test import BaseDirdPhonedIntegrationTest
from .base_dird_phoned_integration_test import DEFAULT_PROFILE
from .base_dird_phoned_integration_test import VALID_TERM
from .base_dird_phoned_integration_test import VALID_USER_AGENT
from .base_dird_phoned_integration_test import VALID_VENDOR
from .base_dird_phoned_integration_test import VALID_XIVO_USER_UUID

from hamcrest import assert_that
from hamcrest import equal_to


class TestStatusCodeDirdPhoned(BaseDirdPhonedIntegrationTest):

    asset = 'default_config'

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
