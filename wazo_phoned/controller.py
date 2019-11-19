# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from xivo import plugin_helpers
from xivo.token_renewer import TokenRenewer
from wazo_auth_client import Client as AuthClient

from .http_server import HTTPServer

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config):
        self.config = config
        self.http_server = HTTPServer(self.config)
        self.http_server.app.config['authorized_subnets'] = self.config['rest_api'][
            'authorized_subnets'
        ]
        self.token_renewer = TokenRenewer(self._new_auth_client(config))
        self.token_renewer.subscribe_to_token_change(self._on_token_change)
        self.plugin_manager = plugin_helpers.load(
            namespace='wazo_phoned.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'config': config,
                'app': self.http_server.app,
                'token_changed_subscribe': self.token_renewer.subscribe_to_token_change,
            },
        )

    def run(self):
        logger.debug('wazo-phoned running...')
        try:
            with self.token_renewer:
                self.http_server.run()
        finally:
            logger.info('wazo-phoned stopping...')
            logger.debug('joining rest api thread...')
            self.http_server.join()
            logger.debug('done joining.')

    def stop(self, reason):
        logger.warning('Stopping wazo-phoned: %s', reason)
        self.http_server.stop()

    def _new_auth_client(self, config):
        auth_config = config['auth']
        return AuthClient(
            auth_config['host'],
            port=auth_config['port'],
            username=auth_config['service_id'],
            password=auth_config['service_key'],
            verify_certificate=auth_config['verify_certificate'],
        )

    def _on_token_change(self, token_id):
        self.http_server.app.config['token'] = token_id
