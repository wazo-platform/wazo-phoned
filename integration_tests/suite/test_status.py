# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    has_entry,
)
from xivo_test_helpers import until

from .helpers.base import BasePhonedIntegrationTest
from .helpers.wait_strategy import PhonedEverythingUpWaitStrategy, PhonedAPIWaitStrategy


class TestStatusNoRabbitMQ(BasePhonedIntegrationTest):

    asset = 'no_rabbitmq'
    wait_strategy = PhonedAPIWaitStrategy()

    def test_given_no_rabbitmq_when_status_then_rabbitmq_fail(self):
        result = self.get_status_result()

        assert_that(result['bus_consumer']['status'], equal_to('fail'))


class TestStatusRabbitMQStops(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_given_rabbitmq_stops_when_status_then_rabbitmq_fail(self):
        self.stop_service('rabbitmq')

        def rabbitmq_is_down():
            result = self.get_status_result()
            assert_that(result['bus_consumer']['status'], equal_to('fail'))

        until.assert_(rabbitmq_is_down, tries=5)


class TestStatusAllOK(BasePhonedIntegrationTest):

    asset = 'default_config'
    wait_strategy = PhonedEverythingUpWaitStrategy()

    def test_given_auth_and_rabbitmq_when_status_then_status_ok(self):

        def all_ok():
            result = self.get_status_result()
            assert_that(result, has_entries(
                bus_consumer=has_entry('status', 'ok'),
                service_token=has_entry('status', 'ok'),
            ))

        until.assert_(all_ok, tries=10)
