# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    empty,
    equal_to,
    has_entries,
    has_item,
)
from textwrap import dedent
from xivo_test_helpers import until

from .helpers.base import (
    BasePhonedIntegrationTest,
    DEFAULT_PROFILE,
    VALID_TERM,
    USER_1_UUID,
)
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

VENDOR = 'yealink'


# NOTE(afournier): these tests should be removed at the same time that the deprecated directories
# route is removed.
class TestYealink(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    # Menu - There is no menu for yealink

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

    # Input - There is no input for yealink

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
        <YealinkIPPhoneDirectory>
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
        </YealinkIPPhoneDirectory>"""
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>No entries</Name>
          <Telephone></Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_shows_first_result(self):
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>Test User1</Name>
          <Telephone>0033123456789</Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_offset_one_shows_middle_result(self):
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>Test User1 (mobile)</Name>
          <Telephone>5555555555</Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_offset_two_shows_last_result(self):
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>Test User2</Name>
          <Telephone>1000</Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>Aucune entrée</Name>
          <Telephone></Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
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


class TestYealinkDirectories(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    # Lookup

    def test_that_lookup_return_no_error_when_query_ssl(self):
        response = self.get_ssl_directories_lookup_result(
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
        <YealinkIPPhoneDirectory>
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
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_that_lookup_return_no_entries_when_no_results(self):
        response = self.get_ssl_directories_lookup_result(
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>No entries</Name>
          <Telephone></Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_shows_first_result(self):
        response = self.get_ssl_directories_lookup_result(
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>Test User1</Name>
          <Telephone>0033123456789</Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_offset_one_shows_middle_result(self):
        response = self.get_ssl_directories_lookup_result(
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>Test User1 (mobile)</Name>
          <Telephone>5555555555</Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_that_lookup_with_limit_one_offset_two_shows_last_result(self):
        response = self.get_ssl_directories_lookup_result(
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>Test User2</Name>
          <Telephone>1000</Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_lookup_translation_fr(self):
        response = self.get_ssl_directories_lookup_result(
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
        <YealinkIPPhoneDirectory>
        <DirectoryEntry>
          <Name>Aucune entrée</Name>
          <Telephone></Telephone>
         </DirectoryEntry>
        </YealinkIPPhoneDirectory>"""
                )
            ),
        )

    def test_that_lookup_return_no_error_when_query(self):
        response = self.get_directories_lookup_result(
            vendor=VENDOR,
            xivo_user_uuid=USER_1_UUID,
            profile=DEFAULT_PROFILE,
            term=VALID_TERM,
        )
        assert_that(response.status_code, equal_to(200))

    def test_that_lookup_return_error_when_no_xivo_user_uuid(self):
        response = self.get_directories_lookup_result(
            vendor=VENDOR, profile=DEFAULT_PROFILE, term=VALID_TERM
        )
        assert_that(response.status_code, equal_to(400))

    def test_that_lookup_return_error_when_invalid_user_uuid(self):
        response = self.get_directories_lookup_result(
            vendor=VENDOR, profile='a', xivo_user_uuid='invalid', term=VALID_TERM
        )
        assert_that(response.status_code, equal_to(404))

    def test_that_lookup_return_error_when_no_term(self):
        response = self.get_directories_lookup_result(
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


class TestUserServiceEvents(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_that_dnd_event_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_dnd_update('123', True)

        def assert_amid_request():
            assert_that(
                amid_client.requests()['requests'],
                has_item(
                    has_entries(
                        {
                            'method': 'POST',
                            'path': '/1.0/action/PJSIPNotify',
                            'json': has_entries(
                                {
                                    'Endpoint': 'line-123',
                                    'Variable': [
                                        'Content-Type=message/sipfrag',
                                        'Event=ACTION-URI',
                                        'Content=key=DNDOn',
                                    ],
                                }
                            ),
                        }
                    )
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_dnd_event_sccp_line_does_not_trigger_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_dnd_update('123-sccp', True)

        def assert_amid_request():
            assert_that(amid_client.requests()['requests'], empty())

        until.assert_(assert_amid_request, tries=5)


class TestUserServiceHTTP(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_dnd_enable(self):
        confd_client = self.make_mock_confd()
        response = self.get_user_service_result(VENDOR, 'dnd', '123', True)
        assert_that(response.status_code, equal_to(200))

        assert_that(
            confd_client.requests()['requests'],
            has_item(
                has_entries(
                    {
                        'method': 'PUT',
                        'path': '/1.1/users/123/services/dnd',
                        'json': has_entries({'enabled': True}),
                    }
                )
            ),
        )

    def test_dnd_disable(self):
        confd_client = self.make_mock_confd()
        response = self.get_user_service_result(VENDOR, 'dnd', '123', False)
        assert_that(response.status_code, equal_to(200))

        assert_that(
            confd_client.requests()['requests'],
            has_item(
                has_entries(
                    {
                        'method': 'PUT',
                        'path': '/1.1/users/123/services/dnd',
                        'json': has_entries({'enabled': False}),
                    }
                )
            ),
        )
