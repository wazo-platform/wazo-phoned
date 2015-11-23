# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


from mock import patch, sentinel as s
from unittest import TestCase

from xivo_dird_phoned.controller import Controller


class TestController(TestCase):

    def setUp(self):
        self.rest_api = patch('xivo_dird_phoned.controller.RestApi').start().return_value
        self.http = patch('xivo_dird_phoned.controller.DirectoriesConfiguration').start()

    def tearDown(self):
        patch.stopall()

    def test_run_starts_rest_api(self):
        config = self._create_config(**{
            'rest_api': {},
            'debug': s.debug,
        })
        controller = Controller(config)
        controller.run()
        self.rest_api.run.assert_called_once_with()

    def test_init_loads_sources(self):
        config = self._create_config()

        Controller(config)

        self.http.assert_called_once_with(config['dird'])

    def _create_config(self, **kwargs):
        config = dict(kwargs)
        config.setdefault('auth', {
            'host': 'localhost',
            'port': 9497,
            'service_id': 'dird-phoned',
            'service_key': '123'}
        )
        config.setdefault('dird', {})
        config['dird'].setdefault('host', '')
        config['dird'].setdefault('port', '')
        config['dird'].setdefault('default_profile', '')
        config.setdefault('rest_api', {})
        config['rest_api'].setdefault('authorized_subnets', [])
        return config
