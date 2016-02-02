# -*- coding: utf-8 -*-
#
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

import logging

from xivo.token_renewer import TokenRenewer
from xivo_auth_client import Client as AuthClient
from xivo_dird_phoned.rest_api import RestApi
from xivo_dird_phoned.http import DirectoriesConfiguration

logger = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, config):
        self.config = config
        self.rest_api = RestApi(self.config['rest_api'])
        self.rest_api.app.config['authorized_subnets'] = self.config['rest_api']['authorized_subnets']
        DirectoriesConfiguration(config['dird'])
        self.token_renewer = TokenRenewer(self._new_auth_client(config))
        self.token_renewer.subscribe_to_token_change(self._on_token_change)

    def run(self):
        logger.debug('xivo-dird-phoned running...')
        try:
            with self.token_renewer:
                self.rest_api.run()
        finally:
            logger.info('xivo-dird-phoned stopping...')

    def _new_auth_client(self, config):
        auth_config = config['auth']
        return AuthClient(auth_config['host'],
                          port=auth_config['port'],
                          username=auth_config['service_id'],
                          password=auth_config['service_key'],
                          verify_certificate=auth_config['verify_certificate'])

    def _on_token_change(self, token_id):
        self.rest_api.app.config['token'] = token_id
