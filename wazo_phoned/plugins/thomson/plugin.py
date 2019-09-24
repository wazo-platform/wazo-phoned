# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugins.proxy_helpers.plugin import ProxyPlugin
from .resource import Lookup


class Plugin(ProxyPlugin):
    vendor = 'thomson'

    def _add_resources(self, api, class_kwargs):
        api.add_resource(
            Lookup,
            self.lookup_url,
            endpoint='thomson_lookup',
            resource_class_kwargs=class_kwargs,
        )
