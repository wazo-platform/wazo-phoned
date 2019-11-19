# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase

from mock import patch, sentinel as s

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
        config.setdefault('rest_api', {})
        config['rest_api'].setdefault('authorized_subnets', [])
        config.setdefault('enabled_plugins', {})
        return config
