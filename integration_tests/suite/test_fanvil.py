# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
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

VENDOR = 'fanvil'


class TestFanvil(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    # Menu - There is no menu for fanvil

    def test_that_menu_return_error_when_query_ssl(self):
        response = self.get_ssl_menu_result(
            vendor=VENDOR, xivo_user_uuid=USER_1_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_menu_return_error_when_query(self):
        response = self.get_menu_result(
            vendor=VENDOR, xivo_user_uuid=USER_1_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(404))

    # Input

    def test_that_input_return_no_error_when_query_ssl(self):
        response = self.get_ssl_input_result(
            vendor=VENDOR, xivo_user_uuid=USER_1_UUID, profile=DEFAULT_PROFILE,
        )
        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            equal_to(
                dedent(
                    """\
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneInputScreen>
                     <Title>Wazo Search</Title>
                     <Prompt>Name or number</Prompt>
                     <URL>https://localhost:{port}/0.1/directories/lookup/{profile}/fanvil?xivo_user_uuid={user_uuid}</URL>
                     <InputItem>
                      <DisplayName>Name or number</DisplayName>
                      <QueryStringParam>term</QueryStringParam>
                      <DefaultValue />
                      <InputFlags>A</InputFlags>
                     </InputItem>
                    </FanvilIPPhoneInputScreen>""".format(
                        port=self.service_port(9499, 'phoned'),
                        profile=DEFAULT_PROFILE,
                        user_uuid=USER_1_UUID,
                    )
                )
            ),
        )

    def test_that_input_return_no_error_when_query(self):
        response = self.get_input_result(
            vendor=VENDOR, xivo_user_uuid=USER_1_UUID, profile=DEFAULT_PROFILE,
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
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <DirectoryEntry>
                      <Name>Test User1</Name>
                      <Telephone>0033123456789</Telephone>
                     </DirectoryEntry>
                    <DirectoryEntry>
                      <Name>Test User1 (mobile)</Name>
                      <Telephone>5555555555</Telephone>
                     </DirectoryEntry>
                    <DirectoryEntry>
                      <Name>Test User2</Name>
                      <Telephone>1000</Telephone>
                     </DirectoryEntry>
                    </FanvilIPPhoneDirectory>"""
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
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <DirectoryEntry>
                      <Name>No entries</Name>
                      <Telephone></Telephone>
                     </DirectoryEntry>
                    </FanvilIPPhoneDirectory>"""
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
                    """\
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <DirectoryEntry>
                      <Name>Test User1</Name>
                      <Telephone>0033123456789</Telephone>
                     </DirectoryEntry>
                    <SoftKeyItem>
                    <Name>Dial</Name>
                    <URL>SoftKey:Dial</URL>
                    <Position>1</Position>
                    </SoftKeyItem>

                    <SoftKeyItem>
                    <Name>Exit</Name>
                    <URL>SoftKey:Exit</URL>
                    <Position>3</Position>
                    </SoftKeyItem>

                    <SoftKeyItem>
                    <Name>NextPage</Name>
                    <URL>https://localhost:{port}/0.1/directories/lookup/{profile}/fanvil?xivo_user_uuid={user_uuid}&term={term}&limit=1&offset=1</URL>
                    <Position>4</Position>
                    </SoftKeyItem>
                    </FanvilIPPhoneDirectory>""".format(
                        port=self.service_port(9499, 'phoned'),
                        profile=DEFAULT_PROFILE,
                        user_uuid=USER_1_UUID,
                        term=VALID_TERM,
                    )
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
                    """\
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <DirectoryEntry>
                      <Name>Test User1 (mobile)</Name>
                      <Telephone>5555555555</Telephone>
                     </DirectoryEntry>
                    <SoftKeyItem>
                    <Name>Dial</Name>
                    <URL>SoftKey:Dial</URL>
                    <Position>1</Position>
                    </SoftKeyItem>

                    <SoftKeyItem>
                    <Name>PrevPage</Name>
                    <URL>https://localhost:{port}/0.1/directories/lookup/{profile}/fanvil?xivo_user_uuid={user_uuid}&term={term}&limit=1&offset=0</URL>
                    <Position>2</Position>
                    </SoftKeyItem>
                    <SoftKeyItem>
                    <Name>Exit</Name>
                    <URL>SoftKey:Exit</URL>
                    <Position>3</Position>
                    </SoftKeyItem>

                    <SoftKeyItem>
                    <Name>NextPage</Name>
                    <URL>https://localhost:{port}/0.1/directories/lookup/{profile}/fanvil?xivo_user_uuid={user_uuid}&term={term}&limit=1&offset=2</URL>
                    <Position>4</Position>
                    </SoftKeyItem>
                    </FanvilIPPhoneDirectory>""".format(
                        port=self.service_port(9499, 'phoned'),
                        profile=DEFAULT_PROFILE,
                        user_uuid=USER_1_UUID,
                        term=VALID_TERM,
                    )
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
                    """\
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <DirectoryEntry>
                      <Name>Test User2</Name>
                      <Telephone>1000</Telephone>
                     </DirectoryEntry>
                    <SoftKeyItem>
                    <Name>Dial</Name>
                    <URL>SoftKey:Dial</URL>
                    <Position>1</Position>
                    </SoftKeyItem>

                    <SoftKeyItem>
                    <Name>PrevPage</Name>
                    <URL>https://localhost:{port}/0.1/directories/lookup/{profile}/fanvil?xivo_user_uuid={user_uuid}&term={term}&limit=1&offset=1</URL>
                    <Position>2</Position>
                    </SoftKeyItem>
                    <SoftKeyItem>
                    <Name>Exit</Name>
                    <URL>SoftKey:Exit</URL>
                    <Position>3</Position>
                    </SoftKeyItem>

                    </FanvilIPPhoneDirectory>""".format(
                        port=self.service_port(9499, 'phoned'),
                        profile=DEFAULT_PROFILE,
                        user_uuid=USER_1_UUID,
                        term=VALID_TERM,
                    )
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
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <DirectoryEntry>
                      <Name>Aucune entrée</Name>
                      <Telephone></Telephone>
                     </DirectoryEntry>
                    </FanvilIPPhoneDirectory>"""
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
            vendor=VENDOR, xivo_user_uuid=USER_1_UUID, profile=DEFAULT_PROFILE,
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
