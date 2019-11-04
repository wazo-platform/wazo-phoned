# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABCMeta, abstractmethod
from wazo_auth_client import Client as AuthClient
from wazo_dird_client import Client as DirdClient

from ..common import create_blueprint_api

import logging

logger = logging.getLogger(__name__)


class ClientPlugin(metaclass=ABCMeta):

    menu_url = '/directories/menu/<profile>/{vendor}'
    input_url = '/directories/input/<profile>/{vendor}'
    lookup_url = '/directories/lookup/<profile>/{vendor}'
    vendor = None
    import_name = None

    def load(self, dependencies):
        app = dependencies['app']
        dird_client = DirdClient(**dependencies['config']['dird'])
        auth_client = AuthClient(**dependencies['config']['auth'])
        token_changed_subscribe = dependencies['token_changed_subscribe']
        token_changed_subscribe(dird_client.set_token)
        token_changed_subscribe(auth_client.set_token)
        class_kwargs = {
            'vendor': self.vendor,
            'dird_client': dird_client,
            'auth_client': auth_client,
        }
        api = create_blueprint_api(
            app, '{}_plugin'.format(self.vendor), self.import_name
        )

        self.menu_url = self.menu_url.format(vendor=self.vendor)
        self.input_url = self.input_url.format(vendor=self.vendor)
        self.lookup_url = self.lookup_url.format(vendor=self.vendor)
        self._add_resources(api, class_kwargs)

    @abstractmethod
    def _add_resources(self, api, class_kwargs):
        pass
