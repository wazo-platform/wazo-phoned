# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase
from unittest.mock import patch

from flask import Flask
from flask_restful import Api
from hamcrest import assert_that, equal_to
from prometheus_client import CollectorRegistry

from ..plugins.metrics.plugin import Plugin


class TestMetricsRestrictedToLocalAndAuthorizedSubnets(TestCase):
    @patch('prometheus_client.REGISTRY', CollectorRegistry())
    def setUp(self):
        app = Flask('test')
        app.config['authorized_subnets'] = ['192.168.0.0/16']
        Plugin().load({'api': Api(app, prefix='/0.1')})
        self.client = app.test_client()

    def test_metrics_from_loopback(self):
        for remote_addr in ('127.0.0.1', '::1'):
            response = self.client.get(
                '/0.1/metrics', environ_base={'REMOTE_ADDR': remote_addr}
            )

            assert_that(response.status_code, equal_to(200), remote_addr)

    def test_metrics_from_an_authorized_subnet(self):
        response = self.client.get(
            '/0.1/metrics', environ_base={'REMOTE_ADDR': '192.168.1.2'}
        )

        assert_that(response.status_code, equal_to(200))

    def test_metrics_from_another_subnet(self):
        response = self.client.get(
            '/0.1/metrics', environ_base={'REMOTE_ADDR': '10.1.2.3'}
        )

        assert_that(response.status_code, equal_to(403))
