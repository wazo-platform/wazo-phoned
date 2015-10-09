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
from .base_dird_phoned_integration_test import VALID_VENDOR
from .base_dird_phoned_integration_test import VALID_XIVO_USER_UUID

from hamcrest import assert_that
from hamcrest import equal_to


class TestSubnetsAuthorized(BaseDirdPhonedIntegrationTest):
    asset = 'no_authorized_subnets'

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_lookup(self):
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE,
                                          term=VALID_TERM)

        assert_that(response.status_code, equal_to(403))

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_menu(self):
        result = self.get_menu_result(vendor=VALID_VENDOR,
                                      xivo_user_uuid=VALID_XIVO_USER_UUID,
                                      profile=DEFAULT_PROFILE)

        assert_that(result.status_code, equal_to(403))

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_ssl_menu(self):
        result = self.get_ssl_menu_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE)

        assert_that(result.status_code, equal_to(403))

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_ssl_lookup(self):
        response = self.get_ssl_lookup_result(vendor=VALID_VENDOR,
                                              xivo_user_uuid=VALID_XIVO_USER_UUID,
                                              profile=DEFAULT_PROFILE,
                                              term=VALID_TERM)

        assert_that(response.status_code, equal_to(403))
