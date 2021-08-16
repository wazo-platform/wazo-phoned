# Copyright 2015-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, equal_to
from textwrap import dedent

from .helpers.base import (
    BasePhonedIntegrationTest,
    DEFAULT_PROFILE,
    VALID_TERM,
    VALID_TERM_NO_LASTNAME,
    USER_1_UUID,
)
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

VENDOR = 'gigaset'


class TestGigaset(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    # Menu - There is no menu for gigaset

    def test_that_menu_return_error_when_query_ssl(self):
        response = self.get_ssl_menu_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_menu_return_error_when_query(self):
        response = self.get_menu_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    # Input - There is no input for gigaset

    def test_that_input_return_error_when_query_ssl(self):
        response = self.get_ssl_input_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_input_return_error_when_query(self):
        response = self.get_input_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    # Lookup

    def test_that_lookup_return_no_error_when_query_ssl(self):
        response = self.get_ssl_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <list response="get_list" type="pr" total="3" first="1" last="3">
                    <entry id="0033123456789">
                    <ln>User1</ln>
                    <fn>Test</fn>
                    <hm>0033123456789</hm>
                    </entry>
                    <entry id="5555555555">
                    <ln>User1 (mobile)</ln>
                    <fn>Test</fn>
                    <hm>5555555555</hm>
                    </entry>
                    <entry id="1000">
                    <ln>User2</ln>
                    <fn>Test</fn>
                    <hm>1000</hm>
                    </entry>
                    </list>"""
                )
            ),
        )

    def test_that_lookup_return_no_error_when_query_ssl_no_lastname(self):
        response = self.get_ssl_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM_NO_LASTNAME,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <list response="get_list" type="pr" total="4" first="1" last="4">
                    <entry id="0033123456789">
                    <ln>User1</ln>
                    <fn>Test</fn>
                    <hm>0033123456789</hm>
                    </entry>
                    <entry id="5555555555">
                    <ln>User1 (mobile)</ln>
                    <fn>Test</fn>
                    <hm>5555555555</hm>
                    </entry>
                    <entry id="1000">
                    <ln>User2</ln>
                    <fn>Test</fn>
                    <hm>1000</hm>
                    </entry>
                    <entry id="1001">
                    <ln></ln>
                    <fn>User3</fn>
                    <hm>1001</hm>
                    </entry>
                    </list>"""
                )
            ),
        )

    def test_that_lookup_return_no_error_when_query_ssl_no_term(self):
        response = self.get_ssl_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <list response="get_list" type="pr" total="3" first="1" last="3">
                    <entry id="0033123456789">
                    <ln>User1</ln>
                    <fn>Test</fn>
                    <hm>0033123456789</hm>
                    </entry>
                    <entry id="5555555555">
                    <ln>User1 (mobile)</ln>
                    <fn>Test</fn>
                    <hm>5555555555</hm>
                    </entry>
                    <entry id="1000">
                    <ln>User2</ln>
                    <fn>Test</fn>
                    <hm>1000</hm>
                    </entry>
                    </list>"""
                )
            ),
        )

    def test_that_lookup_return_no_entries_when_no_results(self):
        response = self.get_ssl_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term='no-result',
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <list response="get_list" type="pr" total="0" first="1" last="0">
                    </list>"""
                )
            ),
        )

    def test_that_lookup_with_count_one_shows_first_result(self):
        response = self.get_ssl_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
            count=1,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <list response="get_list" type="pr" total="3" first="1" last="1">
                    <entry id="0033123456789">
                    <ln>User1</ln>
                    <fn>Test</fn>
                    <hm>0033123456789</hm>
                    </entry>
                    </list>"""
                )
            ),
        )

    def test_that_lookup_with_count_one_first_two_shows_middle_result(self):
        response = self.get_ssl_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
            count=1,
            first=2,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <list response="get_list" type="pr" total="3" first="2" last="2">
                    <entry id="5555555555">
                    <ln>User1 (mobile)</ln>
                    <fn>Test</fn>
                    <hm>5555555555</hm>
                    </entry>
                    </list>"""
                )
            ),
        )

    def test_that_lookup_with_count_one_first_three_shows_last_result(self):
        response = self.get_ssl_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
            count=1,
            first=3,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <?xml version="1.0" encoding="UTF-8"?>
                    <list response="get_list" type="pr" total="3" first="3" last="3">
                    <entry id="1000">
                    <ln>User2</ln>
                    <fn>Test</fn>
                    <hm>1000</hm>
                    </entry>
                    </list>"""
                )
            ),
        )

    # There is no way to test this on Gigaset -- the template does not have strings
    def test_lookup_translation_fr(self):
        pass

    def test_that_lookup_return_no_error_when_query(self):
        response = self.get_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_return_error_when_no_xivo_user_uuid(self):
        response = self.get_lookup_gigaset_result(
            profile=DEFAULT_PROFILE, term=VALID_TERM
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_lookup_return_error_when_invalid_user_uuid(self):
        response = self.get_lookup_gigaset_result(
            profile='a', xivo_user_uuid='invalid', term=VALID_TERM
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_lookup_return_no_error_when_no_term(self):
        response = self.get_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(200))


class TestAuthError(BasePhonedIntegrationTest):

    asset = 'no_auth_server'

    def test_no_auth_server_gives_503(self):
        response = self.get_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term='a',
        )
        assert_that(response.status_code, equal_to(503))


class TestDirdError(BasePhonedIntegrationTest):

    asset = 'no_dird_server'

    def test_no_dird_server_gives_503(self):
        response = self.get_lookup_gigaset_result(
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term='a',
        )
        assert_that(response.status_code, equal_to(503))
