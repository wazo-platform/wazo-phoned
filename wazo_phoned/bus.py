# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import kombu
import logging

from kombu.mixins import ConsumerMixin
from xivo.pubsub import Pubsub
from xivo.status import Status

logger = logging.getLogger(__name__)


class CoreBusConsumer(ConsumerMixin):
    def __init__(self, global_config):
        self._events_pubsub = Pubsub()

        self._bus_url = 'amqp://{username}:{password}@{host}:{port}//'.format(
            **global_config['bus']
        )
        self._exchange = kombu.Exchange(
            global_config['bus']['subscribe_exchange_name'],
            type=global_config['bus']['subscribe_exchange_type'],
        )
        self._queue = kombu.Queue(exclusive=True)
        self._is_running = False

    def run(self):
        logger.info("Running AMQP consumer")
        with kombu.Connection(self._bus_url) as connection:
            self.connection = connection

            super().run()

    def get_consumers(self, Consumer, channel):
        return [Consumer(self._queue, callbacks=[self._on_bus_message])]

    def on_connection_error(self, exc, interval):
        super().on_connection_error(exc, interval)
        self._is_running = False

    def on_connection_revived(self):
        super().on_connection_revived()
        self._is_running = True

    def is_running(self):
        return self._is_running

    def provide_status(self, status):
        status['bus_consumer']['status'] = (
            Status.ok if self.is_running() else Status.fail
        )

    def on_event(self, event_name, callback):
        logger.debug('Added callback on event "%s"', event_name)
        self._queue.bindings.add(
            kombu.binding(
                self._exchange, arguments={'x-match': 'all', 'name': event_name}
            )
        )
        self._events_pubsub.subscribe(event_name, callback)

    def _on_bus_message(self, body, message):
        try:
            event = body['data']
            event_type = event['Event'] if self._is_ami_event(event) else body['name']
        except KeyError:
            logger.error('Invalid event message received: %s', body)
        else:
            self._events_pubsub.publish(event_type, event)
        finally:
            message.ack()

    def _is_ami_event(self, event):
        return 'Event' in event
