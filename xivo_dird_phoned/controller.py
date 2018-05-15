# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

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
            logger.debug('joining rest api thread...')
            self.rest_api.join()
            logger.debug('done joining.')

    def stop(self, reason):
        logger.warning('Stopping xivo-dird-phoned: %s', reason)
        self.rest_api.stop()

    def _new_auth_client(self, config):
        auth_config = config['auth']
        return AuthClient(auth_config['host'],
                          port=auth_config['port'],
                          username=auth_config['service_id'],
                          password=auth_config['service_key'],
                          verify_certificate=auth_config['verify_certificate'])

    def _on_token_change(self, token_id):
        self.rest_api.app.config['token'] = token_id
