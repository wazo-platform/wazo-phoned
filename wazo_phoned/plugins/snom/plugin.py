# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugins.proxy_helpers.plugin import ProxyPlugin
from .resource import Input, Lookup


class Plugin(ProxyPlugin):
    vendor = 'snom'

    def _add_resources(self, api, class_kwargs):
        api.add_resource(
            Input,
            self.input_url,
            endpoint='snom_input',
            resource_class_kwargs=class_kwargs,
        )
        api.add_resource(
            Lookup,
            self.lookup_url,
            endpoint='snom_lookup',
            resource_class_kwargs=class_kwargs,
        )
