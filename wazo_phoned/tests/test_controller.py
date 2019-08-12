# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase

from mock import patch, sentinel as s

from ..controller import Controller


class TestController(TestCase):

    def setUp(self):
        self.http_server = patch('wazo_phoned.controller.HTTPServer').start().return_value
        self.http = patch('wazo_phoned.controller.DirectoriesConfiguration').start()

    def tearDown(self):
        patch.stopall()

    def test_run_starts_http_server(self):
        config = self._create_config(**{
            'rest_api': {},
            'debug': s.debug,
        })
        controller = Controller(config)
        controller.run()
        self.http_server.run.assert_called_once_with()

    def test_init_loads_sources(self):
        config = self._create_config()

        Controller(config)

        self.http.assert_called_once_with(config['dird'])

    def _create_config(self, **kwargs):
        config = dict(kwargs)
        config.setdefault('auth', {
            'host': 'localhost',
            'port': 9497,
            'verify_certificate': False,
            'service_id': 'phoned',
            'service_key': '123'
        })
        config.setdefault('dird', {})
        config['dird'].setdefault('host', '')
        config['dird'].setdefault('port', '')
        config.setdefault('rest_api', {})
        config['rest_api'].setdefault('authorized_subnets', [])
        return config
