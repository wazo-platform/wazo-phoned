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


class TestSubnetsAuthorized(BaseDirdPhonedIntegrationTest):
    asset = 'authorized_subnets'

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_lookup(self):
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE,
                                          term=VALID_TERM)

        assert_that(response.status_code, equal_to(403))

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_lookup_with_extra_header(self):
        headers = {'X-Forwarded-For': '127.0.0.1'}
        response = self.get_lookup_result(vendor=VALID_VENDOR,
                                          xivo_user_uuid=VALID_XIVO_USER_UUID,
                                          profile=DEFAULT_PROFILE,
                                          term=VALID_TERM,
                                          headers=headers)

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
