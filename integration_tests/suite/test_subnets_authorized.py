# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, equal_to

from .helpers.base import (
    DEFAULT_PROFILE,
    USER_1_UUID,
    VALID_TERM,
    VALID_VENDOR,
    BasePhonedIntegrationTest,
)


class TestSubnetsAuthorized(BasePhonedIntegrationTest):
    asset = 'authorized_subnets'

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_lookup(self):
        response = self.get_lookup_result(
            vendor=VALID_VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(403))

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_lookup_with_extra_header(
        self,
    ):
        headers = {'X-Forwarded-For': '127.0.0.1'}
        response = self.get_lookup_result(
            vendor=VALID_VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
            headers=headers,
        )
        assert_that(response.status_code, equal_to(403))

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_menu(self):
        result = self.get_menu_result(
            vendor=VALID_VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(result.status_code, equal_to(403))

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_ssl_menu(self):
        result = self.get_ssl_menu_result(
            vendor=VALID_VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(result.status_code, equal_to(403))

    def test_that_authorized_subnets_do_not_allowed_other_subnets_on_ssl_lookup(self):
        response = self.get_ssl_lookup_result(
            vendor=VALID_VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(403))
