# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_item, has_entries

from .helpers.base import (
    BasePhonedIntegrationTest,
)
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy

from xivo_test_helpers import until


class TestBlf(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_that_dnd_event_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_dnd_update('valid-user-uuid', True)

        def assert_amid_request():
            assert_that(amid_client.requests()['requests'], has_item(has_entries({
                'method': 'POST',
                'path': '/1.0/action/Command',
                'json': has_entries({
                    'command': 'devstate change Custom:*735123***225 INUSE'
                })
            })))

        until.assert_(assert_amid_request, tries=5)

    def test_that_forward_unconditional_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_forward_update('unconditional', 'valid-user-uuid', '1001', True)

        def assert_amid_request():
            assert_that(amid_client.requests()['requests'], has_item(has_entries({
                'method': 'POST',
                'path': '/1.0/action/Command',
                'json': has_entries({
                    'command': 'devstate change Custom:*735123***221*1001 INUSE'
                })
            })))

        until.assert_(assert_amid_request, tries=5)

    def test_that_forward_busy_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_forward_update('busy', 'valid-user-uuid', '1001', True)

        def assert_amid_request():
            assert_that(amid_client.requests()['requests'], has_item(has_entries({
                'method': 'POST',
                'path': '/1.0/action/Command',
                'json': has_entries({
                    'command': 'devstate change Custom:*735123***223*1001 INUSE'
                })
            })))

        until.assert_(assert_amid_request, tries=5)

    def test_that_forward_no_answer_triggers_ami_command(self):
        amid_client = self.make_amid()
        bus_client = self.make_bus()
        bus_client.send_user_forward_update('noanswer', 'valid-user-uuid', '1001', True)

        def assert_amid_request():
            assert_that(amid_client.requests()['requests'], has_item(has_entries({
                'method': 'POST',
                'path': '/1.0/action/Command',
                'json': has_entries({
                    'command': 'devstate change Custom:*735123***222*1001 INUSE'
                })
            })))

        until.assert_(assert_amid_request, tries=5)
