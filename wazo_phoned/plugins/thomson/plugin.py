# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugin_helpers.client.plugin import ClientPlugin
from .http import Lookup


class Plugin(ClientPlugin):
    vendor = 'thomson'
    import_name = __name__

    def _add_resources(self, api, class_kwargs):
        api.add_resource(
            Lookup,
            self.lookup_url,
            endpoint='thomson_lookup',
            resource_class_kwargs=class_kwargs,
        )
