# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugin_helpers.proxy.plugin import ProxyPlugin
from .http import Menu, Input, Lookup


class Plugin(ProxyPlugin):
    vendor = 'cisco'

    def _add_resources(self, api, class_kwargs):
        api.add_resource(
            Menu,
            self.menu_url,
            endpoint='cisco_menu',
            resource_class_kwargs=class_kwargs,
        )
        api.add_resource(
            Input,
            self.input_url,
            endpoint='cisco_input',
            resource_class_kwargs=class_kwargs,
        )
        api.add_resource(
            Lookup,
            self.lookup_url,
            endpoint='cisco_lookup',
            resource_class_kwargs=class_kwargs,
        )
