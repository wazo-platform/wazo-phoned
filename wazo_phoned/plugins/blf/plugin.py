# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_amid_client import Client as AmidClient
from wazo_confd_client import Client as ConfdClient

from .bus_consume import BusEventHandler
from .services import BlfService


class Plugin:

    def load(self, dependencies):
        amid_client = AmidClient(**dependencies['config']['amid'])
        confd_client = ConfdClient(**dependencies['config']['confd'])
        token_changed_subscribe = dependencies['token_changed_subscribe']
        token_changed_subscribe(amid_client.set_token)
        token_changed_subscribe(confd_client.set_token)

        bus_consumer = dependencies['bus_consumer']

        service = BlfService(amid_client, confd_client)

        bus_event_handler = BusEventHandler(service)
        bus_event_handler.subscribe(bus_consumer)
