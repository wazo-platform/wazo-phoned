# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from threading import Thread
from xivo import plugin_helpers
from xivo.config_helper import set_xivo_uuid
from xivo.status import StatusAggregator, TokenStatus
from xivo.token_renewer import TokenRenewer
from wazo_auth_client import Client as AuthClient

from .bus import CoreBusConsumer
from .bus import CoreBusPublisher
from .http_server import HTTPServer

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config):
        self.config = config
        set_xivo_uuid(config, logger)
        self.bus_publisher = CoreBusPublisher(config)
        self.bus_consumer = CoreBusConsumer(config)
        self.status_aggregator = StatusAggregator()
        self.http_server = HTTPServer(self.config)
        self.http_server.app.config['authorized_subnets'] = self.config['rest_api'][
            'authorized_subnets'
        ]
        self.token_renewer = TokenRenewer(self._new_auth_client(config))
        self.token_renewer.subscribe_to_token_change(self._on_token_change)

        self.token_status = TokenStatus()
        self.token_renewer.subscribe_to_token_change(self.token_status.token_change_callback)

        self.plugin_manager = plugin_helpers.load(
            namespace='wazo_phoned.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'config': config,
                'app': self.http_server.app,
                'token_changed_subscribe': self.token_renewer.subscribe_to_token_change,
                'bus_publisher': self.bus_publisher,
                'bus_consumer': self.bus_consumer,
                'status_aggregator': self.status_aggregator,
            },
        )

    def run(self):
        logger.debug('wazo-phoned starting...')
        self.status_aggregator.add_provider(self.bus_consumer.provide_status)
        self.status_aggregator.add_provider(self.token_status.provide_status)
        bus_producer_thread = Thread(target=self.bus_publisher.run, name='bus_producer_thread')
        bus_producer_thread.start()
        bus_consumer_thread = Thread(target=self.bus_consumer.run, name='bus_consumer_thread')
        bus_consumer_thread.start()
        try:
            with self.token_renewer:
                self.http_server.run()
        finally:
            logger.info('wazo-phoned stopping...')
            self.bus_consumer.should_stop = True
            self.bus_publisher.stop()
            logger.debug('joining rest api thread...')
            self.http_server.join()
            logger.debug('joining bus consumer thread...')
            bus_consumer_thread.join()
            logger.debug('joining bus producer thread...')
            bus_producer_thread.join()
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
