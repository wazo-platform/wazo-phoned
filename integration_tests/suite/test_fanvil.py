# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from textwrap import dedent

from hamcrest import assert_that, empty, equal_to, has_entries, has_item
from wazo_test_helpers import until

from .helpers.base import (
    DEFAULT_PROFILE,
    USER_1_UUID,
    VALID_TERM,
    BasePhonedIntegrationTest,
)
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

VENDOR = 'fanvil'


class TestFanvil(BasePhonedIntegrationTest):
    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    # Menu - There is no menu for fanvil

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
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneInputScreen>
                     <Title>Wazo Search</Title>
                     <Prompt>Name or number</Prompt>
                     <URL>https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/fanvil?xivo_user_uuid={USER_1_UUID}</URL>
                     <InputField>
                      <Prompt>Name or number</Prompt>
                      <Parameter>term</Parameter>
                      <Default></Default>
                     </InputField>
                    </FanvilIPPhoneInputScreen>"""
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
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <MenuItem>
                      <Prompt>Test User1</Prompt>
                      <URI>0033123456789</URI>
                     </MenuItem>
                    <MenuItem>
                      <Prompt>Test User1 (mobile)</Prompt>
                      <URI>5555555555</URI>
                     </MenuItem>
                    <MenuItem>
                      <Prompt>Test User2</Prompt>
                      <URI>1000</URI>
                     </MenuItem>
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
                    <MenuItem>
                      <Prompt>No entries</Prompt>
                      <URI></URI>
                     </MenuItem>
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
                    f"""\
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <MenuItem>
                      <Prompt>Test User1</Prompt>
                      <URI>0033123456789</URI>
                     </MenuItem>
                    <SoftKey>
                    <Name>Dial</Name>
                    <URI>SoftKey:Dial</URI>
                    </SoftKey>

                    <SoftKey>
                    <Name>Exit</Name>
                    <URI>SoftKey:Exit</URI>
                    </SoftKey>

                    <SoftKey>
                    <Name>NextPage</Name>
                    <URI>https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/fanvil?xivo_user_uuid={USER_1_UUID}&amp;term={VALID_TERM}&amp;limit=1&amp;offset=1</URI>
                    </SoftKey>
                    </FanvilIPPhoneDirectory>"""
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
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <MenuItem>
                      <Prompt>Test User1 (mobile)</Prompt>
                      <URI>5555555555</URI>
                     </MenuItem>
                    <SoftKey>
                    <Name>Dial</Name>
                    <URI>SoftKey:Dial</URI>
                    </SoftKey>

                    <SoftKey>
                    <Name>PrevPage</Name>
                    <URI>https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/fanvil?xivo_user_uuid={USER_1_UUID}&amp;term={VALID_TERM}&amp;limit=1&amp;offset=0</URI>
                    </SoftKey>
                    <SoftKey>
                    <Name>Exit</Name>
                    <URI>SoftKey:Exit</URI>
                    </SoftKey>

                    <SoftKey>
                    <Name>NextPage</Name>
                    <URI>https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/fanvil?xivo_user_uuid={USER_1_UUID}&amp;term={VALID_TERM}&amp;limit=1&amp;offset=2</URI>
                    </SoftKey>
                    </FanvilIPPhoneDirectory>"""
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
                    <?xml version="1.0" encoding="UTF-8" ?>
                    <FanvilIPPhoneDirectory>
                    <MenuItem>
                      <Prompt>Test User2</Prompt>
                      <URI>1000</URI>
                     </MenuItem>
                    <SoftKey>
                    <Name>Dial</Name>
                    <URI>SoftKey:Dial</URI>
                    </SoftKey>

                    <SoftKey>
                    <Name>PrevPage</Name>
                    <URI>https://127.0.0.1:{self.service_port(9499, 'phoned')}/0.1/directories/lookup/{DEFAULT_PROFILE}/fanvil?xivo_user_uuid={USER_1_UUID}&amp;term={VALID_TERM}&amp;limit=1&amp;offset=1</URI>
                    </SoftKey>
                    <SoftKey>
                    <Name>Exit</Name>
                    <URI>SoftKey:Exit</URI>
                    </SoftKey>

                    </FanvilIPPhoneDirectory>"""
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
                    <MenuItem>
                      <Prompt>Aucune entrée</Prompt>
                      <URI></URI>
                     </MenuItem>
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
        endpoint_name = '234'
        bus_client.send_user_dnd_update(endpoint_name, True)

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
                                    'Endpoint': f'line-{endpoint_name}',
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
        user_uuid = '234'
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_dnd_update(f'{user_uuid}-sccp', True)

        def assert_amid_request():
            assert_that(amid_client.requests()['requests'], empty())

        until.assert_(assert_amid_request, tries=5)


class TestUserServiceHTTP(BasePhonedIntegrationTest):
    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_dnd_enable(self):
        user_uuid = '234'
        confd_client = self.make_mock_confd()
        confd_client.set_user_service(user_uuid, 'dnd', False)
        bus_client = self.make_bus()
        bus_client.send_user_dnd_update(user_uuid, False)
        response = self.get_user_service_result(VENDOR, 'dnd', user_uuid, True)
        assert_that(response.status_code, equal_to(200))

        assert_that(
            confd_client.requests()['requests'],
            has_item(
                has_entries(
                    {
                        'method': 'PUT',
                        'path': f'/1.1/users/{user_uuid}/services/dnd',
                        'json': has_entries({'enabled': True}),
                    }
                )
            ),
        )

    def test_dnd_disable(self):
        user_uuid = '234'
        confd_client = self.make_mock_confd()
        confd_client.set_user_service(user_uuid, 'dnd', True)
        bus_client = self.make_bus()
        bus_client.send_user_dnd_update(user_uuid, True)
        response = self.get_user_service_result(VENDOR, 'dnd', user_uuid, False)
        assert_that(response.status_code, equal_to(200))

        assert_that(
            confd_client.requests()['requests'],
            has_item(
                has_entries(
                    {
                        'method': 'PUT',
                        'path': f'/1.1/users/{user_uuid}/services/dnd',
                        'json': has_entries({'enabled': False}),
                    }
                )
            ),
        )
