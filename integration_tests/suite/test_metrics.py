# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, contains_string, equal_to

from .helpers.base import BasePhonedIntegrationTest
from .helpers.wait_strategy import PhonedAPIWaitStrategy


class TestMetrics(BasePhonedIntegrationTest):
    asset = 'default_config'
    wait_strategy = PhonedAPIWaitStrategy()

    def test_metrics_without_token_from_an_authorized_subnet(self):
        self.get_status_result()

        response = self.get_metrics_result()

        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.text,
            contains_string('flask_http_request_total{method="GET",status="200"}'),
        )
        assert_that(
            response.text,
            contains_string(
                'flask_http_request_duration_seconds_count'
                '{endpoint="status_plugin.status",method="GET",status="200"}'
            ),
        )
