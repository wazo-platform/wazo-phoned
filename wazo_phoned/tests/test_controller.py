# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase

from mock import Mock, patch, sentinel as s
from xivo import config_helper

from ..controller import Controller


class TestController(TestCase):
    def setUp(self):
        self.http_server = (
            patch('wazo_phoned.controller.HTTPServer').start().return_value
        )
        self.plugin_manager = patch('wazo_phoned.controller.plugin_helpers').start()
        self.token_renewer = (
            patch('wazo_phoned.controller.TokenRenewer').start().return_value
        )
        self.bus_consumer = (
            patch('wazo_phoned.controller.CoreBusConsumer').start().return_value
        )
        self.status_aggregator = (
            patch('wazo_phoned.controller.StatusAggregator').start().return_value
        )
        config_helper.get_xivo_uuid = Mock(return_value='VALID-UUID')

    def tearDown(self):
        patch.stopall()

    def test_run_starts_http_server(self):
        config = self._create_config(**{'rest_api': {}, 'debug': s.debug})
        controller = Controller(config)
        controller.run()
        self.http_server.run.assert_called_once_with()

    def test_run_loads_plugins(self):
        config = self._create_config(
            **{'enabled_plugins': {'cisco': True, 'aastra': False}}
        )

        controller = Controller(config)
        controller.run()

        self.plugin_manager.load.assert_called_once_with(
            namespace='wazo_phoned.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'config': config,
                'app': self.http_server.app,
                'token_changed_subscribe': self.token_renewer.subscribe_to_token_change,
                'bus_consumer': self.bus_consumer,
                'status_aggregator': self.status_aggregator,
                'phone_plugins': controller.phone_plugins,
            },
        )

    def _create_config(self, **kwargs):
        config = dict(kwargs)
        config.setdefault(
            'auth',
            {
                'host': 'localhost',
                'port': 9497,
                'verify_certificate': False,
                'service_id': 'phoned',
                'service_key': '123',
            },
        )
        config.setdefault('dird', {})
        config['dird'].setdefault('host', '')
        config['dird'].setdefault('port', '')
        config.setdefault(
            'bus',
            {
                'username': 'guest',
                'password': 'guest',
                'host': 'localhost',
                'port': 5672,
                'subscribe_exchange_name': 'wazo-headers',
                'subscribe_exchange_type': 'headers',
            },
        )
        config.setdefault('rest_api', {})
        config['rest_api'].setdefault('authorized_subnets', [])
        config.setdefault('enabled_plugins', {})
        return config
