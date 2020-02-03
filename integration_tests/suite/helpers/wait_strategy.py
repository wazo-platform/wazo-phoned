# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, only_contains, has_property
from requests import ConnectionError, RequestException
from xivo_test_helpers import until
from xivo_test_helpers.wait_strategy import WaitStrategy


class PhonedEverythingUpWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def everything_is_up():
            try:
                status = integration_test.get_status_result_by_https()
            except RequestException as e:
                raise AssertionError('wazo-phoned is not up yet: {}'.format(e))
            component_statuses = [
                component['status']
                for component in status.values()
                if 'status' in component
            ]
            assert_that(component_statuses, only_contains('ok'))

        until.assert_(everything_is_up, timeout=10)


class PhonedAPIWaitStrategy(WaitStrategy):
    def wait(self, integration_test):
        def api_is_up():
            try:
                status = integration_test.get_status_result_by_https()
            except ConnectionError as e:
                raise AssertionError('wazo-phoned is not up yet: {}'.format(e))

        until.assert_(api_is_up, timeout=10)
