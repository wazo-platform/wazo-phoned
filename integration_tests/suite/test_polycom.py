# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, equal_to
from textwrap import dedent

from .helpers.base import (
    BasePhonedIntegrationTest,
    DEFAULT_PROFILE,
    VALID_TERM,
    USER_1_UUID,
)
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

VENDOR = 'polycom'


class TestPolycom(BasePhonedIntegrationTest):
    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    # Menu - There is no menu for polycom

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

    # Input

    def test_that_input_return_no_error_when_query_ssl(self):
        response = self.get_ssl_input_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    f"""\
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                    <html>
                      <head>
                        <title>Wazo Search</title>
                      </head>
                      <body>
                        <form action="https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/polycom" method="get" accept-charset="utf-8">
                          <span>
                            <label for="it-term">Name or number:</label>
                          </span>
                          <input type="text" name="term" id="it-term" size="15" value="" />
                          <input type="hidden" name="xivo_user_uuid" value="{USER_1_UUID}" />
                          <input type="submit" name="submit" value="Search" />
                        </form>
                      </body>
                    </html>"""
                )
            ),
        )

    def test_that_input_return_no_error_when_query(self):
        response = self.get_input_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(200))

    def test_that_input_return_error_when_no_xivo_user_uuid(self):
        response = self.get_input_result(vendor=VENDOR, profile=DEFAULT_PROFILE)
        assert_that(response.status_code, equal_to(400))

    # Lookup

    def test_that_lookup_return_no_error_when_query_ssl(self):
        response = self.get_ssl_lookup_result(
            vendor=VENDOR,
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
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                    <html>
                      <head>
                        <title>Wazo Search</title>
                      </head>
                      <body>
                        <ol>
                    <li><a href="tel://0033123456789">Test User1</a><br /></li>
                    <li><a href="tel://5555555555">Test User1 (mobile)</a><br /></li>
                    <li><a href="tel://1000">Test User2</a><br /></li>
                    </ol>
                      </body>
                    </html>"""
                )
            ),
        )

    def test_that_lookup_return_no_entries_when_no_results(self):
        response = self.get_ssl_lookup_result(
            vendor=VENDOR,
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
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                    <html>
                      <head>
                        <title>Wazo Search</title>
                      </head>
                      <body>
                        <ol>
                    <li>No entries<br /></li>
                    </ol>
                      </body>
                    </html>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_shows_next_page_link(self):
        response = self.get_ssl_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
            limit=1,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    f"""\
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                    <html>
                      <head>
                        <title>Wazo Search</title>
                      </head>
                      <body>
                        <ol>
                    <li><a href="tel://0033123456789">Test User1</a><br /></li>
                    <li>[<a href="https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/polycom?xivo_user_uuid={USER_1_UUID}&amp;term={VALID_TERM}&amp;limit=1&amp;offset=1" title="Next">Next Page</a>]<br /></li>
                    </ol>
                      </body>
                    </html>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_offset_one_shows_previous_and_next_page_links(
        self,
    ):
        response = self.get_ssl_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
            limit=1,
            offset=1,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    f"""\
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                    <html>
                      <head>
                        <title>Wazo Search</title>
                      </head>
                      <body>
                        <ol>
                    <li>[<a href="https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/polycom?xivo_user_uuid={USER_1_UUID}&amp;term={VALID_TERM}&amp;limit=1&amp;offset=0" title="Previous">Previous Page</a>]<br /></li>
                    <li><a href="tel://5555555555">Test User1 (mobile)</a><br /></li>
                    <li>[<a href="https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/polycom?xivo_user_uuid={USER_1_UUID}&amp;term={VALID_TERM}&amp;limit=1&amp;offset=2" title="Next">Next Page</a>]<br /></li>
                    </ol>
                      </body>
                    </html>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_offset_two_shows_previous_page_link(self):
        response = self.get_ssl_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
            limit=1,
            offset=2,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    f"""\
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                    <html>
                      <head>
                        <title>Wazo Search</title>
                      </head>
                      <body>
                        <ol>
                    <li>[<a href="https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/polycom?xivo_user_uuid={USER_1_UUID}&amp;term={VALID_TERM}&amp;limit=1&amp;offset=1" title="Previous">Previous Page</a>]<br /></li>
                    <li><a href="tel://1000">Test User2</a><br /></li>
                    </ol>
                      </body>
                    </html>"""
                )
            ),
        )

    def test_lookup_translation_fr(self):
        response = self.get_ssl_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term='no-result',
            headers={'Accept-Language': 'gibberish,fr-CA,*q=nothing'},
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                    <html>
                      <head>
                        <title>Recherche Wazo</title>
                      </head>
                      <body>
                        <ol>
                    <li>Aucune entrée<br /></li>
                    </ol>
                      </body>
                    </html>"""
                )
            ),
        )

    def test_that_lookup_return_no_error_when_query(self):
        response = self.get_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_return_error_when_no_xivo_user_uuid(self):
        response = self.get_lookup_result(
            vendor=VENDOR, profile=DEFAULT_PROFILE, term=VALID_TERM
        )
        assert_that(response.status_code, equal_to(400))

    def test_that_lookup_return_error_when_invalid_user_uuid(self):
        response = self.get_lookup_result(
            vendor=VENDOR, profile='a', xivo_user_uuid='invalid', term=VALID_TERM
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_lookup_return_error_when_no_term(self):
        response = self.get_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(400))


class TestAuthError(BasePhonedIntegrationTest):
    asset = 'no_auth_server'

    def test_no_auth_server_gives_503(self):
        response = self.get_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term='a',
        )
        assert_that(response.status_code, equal_to(503))


class TestDirdError(BasePhonedIntegrationTest):
    asset = 'no_dird_server'

    def test_no_dird_server_gives_503(self):
        response = self.get_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term='a',
        )
        assert_that(response.status_code, equal_to(503))
