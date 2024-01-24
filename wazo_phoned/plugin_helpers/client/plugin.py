# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from abc import ABCMeta, abstractmethod

from wazo_auth_client import Client as AuthClient
from wazo_dird_client import Client as DirdClient

from ..common import create_blueprint_api

logger = logging.getLogger(__name__)


class ClientPlugin(metaclass=ABCMeta):
    # NOTE(afournier): these vendor-ending URLs are deprecated and will be phased out gradually
    menu_url_fmt = '/directories/menu/<profile>/{vendor}'
    input_url_fmt = '/directories/input/<profile>/{vendor}'
    lookup_url_fmt = '/directories/lookup/<profile>/{vendor}'

    directories_menu_url_fmt = '{vendor}/directories/menu/<profile>'
    directories_input_url_fmt = '{vendor}/directories/input/<profile>'
    directories_lookup_url_fmt = '{vendor}/directories/lookup/<profile>'
    vendor = None
    import_name = None

    def load(self, dependencies):
        app = dependencies['app']
        dird_client = DirdClient(**dependencies['config']['dird'])
        auth_client = AuthClient(**dependencies['config']['auth'])
        token_changed_subscribe = dependencies['token_changed_subscribe']
        token_changed_subscribe(dird_client.set_token)
        token_changed_subscribe(auth_client.set_token)
        dependencies['phone_plugins'].append(self)
        class_kwargs = {
            'vendor': self.vendor,
            'dird_client': dird_client,
            'auth_client': auth_client,
        }
        api = create_blueprint_api(app, f'{self.vendor}_plugin', self.import_name)

        self.menu_url = self.menu_url_fmt.format(vendor=self.vendor)
        self.input_url = self.input_url_fmt.format(vendor=self.vendor)
        self.lookup_url = self.lookup_url_fmt.format(vendor=self.vendor)

        self.directories_menu_url = self.directories_menu_url_fmt.format(
            vendor=self.vendor
        )
        self.directories_input_url = self.directories_input_url_fmt.format(
            vendor=self.vendor
        )
        self.directories_lookup_url = self.directories_lookup_url_fmt.format(
            vendor=self.vendor
        )
        self._add_resources(api, class_kwargs)

    @abstractmethod
    def _add_resources(self, api, class_kwargs):
        pass

    def match_vendor(self, vendor):
        return vendor.strip().lower() == self.vendor
