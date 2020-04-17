# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from kombu import Connection
from kombu import Exchange
from kombu import Producer
from xivo_test_helpers import bus as bus_helper


BUS_EXCHANGE_HEADERS = Exchange('wazo-headers', type='headers')
BUS_URL = 'amqp://guest:guest@localhost:5672//'
BUS_QUEUE_NAME = 'integration'


class BusClient(bus_helper.BusClient):
    def send_event(self, event):
        with Connection(self._url) as connection:
            producer = Producer(
                connection, exchange=BUS_EXCHANGE_HEADERS, auto_declare=True
            )
            producer.publish(
                json.dumps(event),
                headers={'name': event['name']},
                content_type='application/json',
            )

    def send_user_dnd_update(self, user_id, enabled):
        self.send_event(
            {
                'name': 'users_services_dnd_updated',
                'data': {'user_id': user_id, 'user_uuid': user_id, 'enabled': enabled},
            }
        )

    def send_user_incallfilter_update(self, user_id, enabled):
        self.send_event(
            {
                'name': 'users_services_incallfilter_updated',
                'data': {'user_id': user_id, 'user_uuid': user_id, 'enabled': enabled},
            }
        )

    def send_user_forward_update(self, forward_name, user_id, destination, enabled):
        self.send_event(
            {
                'name': 'users_forwards_{}_updated'.format(forward_name),
                'data': {
                    'user_id': user_id,
                    'user_uuid': user_id,
                    'destination': destination,
                    'enabled': enabled,
                },
            }
        )

    def send_extension_feature_edited(self):
        self.send_event({'name': 'extension_feature_edited', 'data': {'id': 1234}})
