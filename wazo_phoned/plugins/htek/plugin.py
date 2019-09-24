# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugin_helpers.proxy.plugin import ProxyPlugin
from .resource import Lookup


class Plugin(ProxyPlugin):
    vendor = 'htek'

    def _add_resources(self, api, class_kwargs):
        api.add_resource(
            Lookup,
            self.lookup_url,
            endpoint='htek_lookup',
            resource_class_kwargs=class_kwargs,
        )
