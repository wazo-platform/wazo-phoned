# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    has_item,
)
from xivo_test_helpers import until

from .helpers.base import (
    BasePhonedIntegrationTest,
    VALID_TOKEN,
)
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy


class TestEndpointHoldHTTP(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_that_endpoint_hold_start_sends_ami_command(self):
        amid_client = self.make_amid()
        response = self.get_endpoint_hold_start_result('yealink', VALID_TOKEN)
        assert_that(response.status_code, equal_to(204))

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
                                    'Endpoint': 'yealink',
                                    'Variable': [
                                        'Content-Type=message/sipfrag',
                                        'Event=ACTION-URI',
                                        'Content=key=F_HOLD',
                                    ],
                                }
                            ),
                        }
                    )
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_endpoint_hold_stop_sends_ami_command(self):
        amid_client = self.make_amid()
        response = self.get_endpoint_hold_stop_result('yealink', VALID_TOKEN)
        assert_that(response.status_code, equal_to(204))

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
                                    'Endpoint': 'yealink',
                                    'Variable': [
                                        'Content-Type=message/sipfrag',
                                        'Event=ACTION-URI',
                                        'Content=key=F_HOLD',  # Yes, for Yealink it's the same key
                                    ],
                                }
                            ),
                        }
                    )
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_endpoint_hold_start_with_invalid_device_returns_404(self):
        response = self.get_endpoint_hold_start_result('unknown', VALID_TOKEN)
        assert_that(response.status_code, equal_to(404))
        assert_that(response.json(), has_entries({'error_id': 'unknown-device'}))

    def test_that_endpoint_hold_start_with_unknown_vendor_raises_400(self):
        response = self.get_endpoint_hold_start_result('unknown-vendor', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))

    def test_that_hold_start_non_existing_endpoint_returns_404(self):
        response = self.get_endpoint_hold_start_result('no-result', VALID_TOKEN)
        assert_that(response.status_code, equal_to(404))
        assert_that(response.json(), has_entries({'error_id': 'unknown-endpoint'}))

    def test_that_hold_start_endpoint_requires_valid_token(self):
        response = self.get_endpoint_hold_start_result('yealink', 'invalid-token')
        assert_that(response.status_code, equal_to(401))

    def test_that_hold_start_endpoint_no_service_raises_400(self):
        # NOTE(afournier): make sure that the tested plugin does not support hold
        response = self.get_endpoint_hold_start_result('cisco', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))

    def test_that_hold_start_endpoint_empty_vendor_raises_400(self):
        response = self.get_endpoint_hold_start_result('empty-vendor', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))

    def test_that_endpoint_hold_stop_with_invalid_device_returns_404(self):
        response = self.get_endpoint_hold_stop_result('unknown', VALID_TOKEN)
        assert_that(response.status_code, equal_to(404))
        assert_that(response.json(), has_entries({'error_id': 'unknown-device'}))

    def test_that_endpoint_hold_stop_with_unknown_vendor_raises_400(self):
        response = self.get_endpoint_hold_stop_result('unknown-vendor', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))

    def test_that_hold_stop_non_existing_endpoint_returns_404(self):
        response = self.get_endpoint_hold_stop_result('no-result', VALID_TOKEN)
        assert_that(response.status_code, equal_to(404))
        assert_that(response.json(), has_entries({'error_id': 'unknown-endpoint'}))

    def test_that_hold_stop_endpoint_requires_valid_token(self):
        response = self.get_endpoint_hold_stop_result('yealink', 'invalid-token')
        assert_that(response.status_code, equal_to(401))

    def test_that_hold_stop_endpoint_no_service_raises_400(self):
        # NOTE(afournier): make sure that the tested plugin does not support hold
        response = self.get_endpoint_hold_stop_result('cisco', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))

    def test_that_hold_stop_endpoint_empty_vendor_raises_400(self):
        response = self.get_endpoint_hold_stop_result('empty-vendor', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))


class TestEndpointAnswerHTTP(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_that_endpoint_hold_start_sends_ami_command(self):
        amid_client = self.make_amid()
        response = self.get_endpoint_answer_result('yealink', VALID_TOKEN)
        assert_that(response.status_code, equal_to(204))

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
                                    'Endpoint': 'yealink',
                                    'Variable': [
                                        'Content-Type=message/sipfrag',
                                        'Event=ACTION-URI',
                                        'Content=key=ANSWER',
                                    ],
                                }
                            ),
                        }
                    )
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_endpoint_answer_with_invalid_device_returns_404(self):
        response = self.get_endpoint_answer_result('unknown', VALID_TOKEN)
        assert_that(response.status_code, equal_to(404))
        assert_that(response.json(), has_entries({'error_id': 'unknown-device'}))

    def test_that_endpoint_answer_with_unknown_vendor_raises_400(self):
        response = self.get_endpoint_answer_result('unknown-vendor', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))

    def test_that_answer_non_existing_endpoint_returns_404(self):
        response = self.get_endpoint_answer_result('no-result', VALID_TOKEN)
        assert_that(response.status_code, equal_to(404))
        assert_that(response.json(), has_entries({'error_id': 'unknown-endpoint'}))

    def test_that_answer_endpoint_requires_valid_token(self):
        response = self.get_endpoint_answer_result('yealink', 'invalid-token')
        assert_that(response.status_code, equal_to(401))

    def test_that_answer_endpoint_no_service_raises_400(self):
        # NOTE(afournier): make sure that the tested plugin does not support hold
        response = self.get_endpoint_answer_result('cisco', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))

    def test_that_answer_endpoint_empty_vendor_raises_400(self):
        response = self.get_endpoint_answer_result('empty-vendor', VALID_TOKEN)
        assert_that(response.status_code, equal_to(400))
