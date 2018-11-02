# Copyright 2015-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import time

from hamcrest import (
    assert_that,
    contains_string,
)

from .base_dird_phoned_integration_test import BaseDirdPhonedIntegrationTest


class TestMissingServiceKeyFile(BaseDirdPhonedIntegrationTest):
    asset = 'no_service_key'

    def test_given_inexisting_service_key_when_dird_phoned_starts_then_dird_phoned_stops(self):
        for _ in range(5):
            status = self.service_status('phoned')
            if not status['State']['Running']:
                break
            time.sleep(1)
        else:
            self.fail('xivo-dird-phoned did not stop while missing service key file')

        log = self.service_logs('phoned')
        assert_that(log, contains_string("No such file or directory: '/tmp/not_exists/xivo-dird-phoned-key.yml'"))
