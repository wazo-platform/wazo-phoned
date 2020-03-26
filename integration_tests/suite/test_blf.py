# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_item, has_items, has_entries, not_

from .helpers.base import BasePhonedIntegrationTest
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

from xivo_test_helpers import until


class TestBlf(BasePhonedIntegrationTest):

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
                            'path': '/1.0/action/Command',
                            'json': has_entries(
                                {
                                    'command': 'devstate change Custom:*735123***225 INUSE'
                                }
                            ),
                        }
                    )
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_incallfilter_event_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_incallfilter_update('123', True)

        def assert_amid_request():
            assert_that(
                amid_client.requests()['requests'],
                has_item(
                    has_entries(
                        {
                            'method': 'POST',
                            'path': '/1.0/action/Command',
                            'json': has_entries(
                                {
                                    'command': 'devstate change Custom:*735123***227 INUSE'
                                }
                            ),
                        }
                    )
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_forward_unconditional_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_forward_update('unconditional', '123', '1001', True)

        def assert_amid_request():
            assert_that(
                amid_client.requests()['requests'],
                has_items(
                    has_entries(
                        {
                            'method': 'POST',
                            'path': '/1.0/action/Command',
                            'json': has_entries(
                                {
                                    'command': 'devstate change Custom:*735123***221*1001 INUSE'
                                }
                            ),
                        }
                    ),
                    has_entries(
                        {
                            'method': 'POST',
                            'path': '/1.0/action/Command',
                            'json': has_entries(
                                {
                                    'command': 'devstate change Custom:*735123***221 INUSE'
                                }
                            ),
                        }
                    ),
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_forward_busy_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_forward_update('busy', '123', '1001', True)

        def assert_amid_request():
            assert_that(
                amid_client.requests()['requests'],
                has_items(
                    has_entries(
                        {
                            'method': 'POST',
                            'path': '/1.0/action/Command',
                            'json': has_entries(
                                {
                                    'command': 'devstate change Custom:*735123***223*1001 INUSE'
                                }
                            ),
                        }
                    ),
                    has_entries(
                        {
                            'method': 'POST',
                            'path': '/1.0/action/Command',
                            'json': has_entries(
                                {
                                    'command': 'devstate change Custom:*735123***223 INUSE'
                                }
                            ),
                        }
                    ),
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_forward_no_answer_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_forward_update('noanswer', '123', '1001', True)

        def assert_amid_request():
            assert_that(
                amid_client.requests()['requests'],
                has_items(
                    has_entries(
                        {
                            'method': 'POST',
                            'path': '/1.0/action/Command',
                            'json': has_entries(
                                {
                                    'command': 'devstate change Custom:*735123***222*1001 INUSE'
                                }
                            ),
                        }
                    ),
                    has_entries(
                        {
                            'method': 'POST',
                            'path': '/1.0/action/Command',
                            'json': has_entries(
                                {
                                    'command': 'devstate change Custom:*735123***222 INUSE'
                                }
                            ),
                        }
                    ),
                ),
            )

        until.assert_(assert_amid_request, tries=5)

    def test_that_extensions_features_are_cached(self):
        bus_client = self.make_bus()
        confd_client = self.make_mock_confd()
        bus_client.send_extension_feature_edited()
        bus_client.send_user_dnd_update('123', True)

        def assert_extensions_features():
            assert_that(
                confd_client.requests()['requests'],
                has_item(
                    has_entries({'method': 'GET', 'path': '/1.1/extensions/features'})
                ),
            )

        until.assert_(assert_extensions_features, tries=5)

        confd_client.reset()
        bus_client.send_user_dnd_update('123', True)

        def assert_no_extensions_features():
            assert_that(
                confd_client.requests()['requests'],
                not_(
                    has_item(
                        has_entries(
                            {'method': 'GET', 'path': '/1.1/extensions/features'}
                        )
                    )
                ),
            )

        until.assert_(assert_no_extensions_features, tries=5)
