# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugin_helpers.client.plugin import ClientPlugin

from .http import Input, Lookup


class Plugin(ClientPlugin):
    vendor = 'fanvil'
    import_name = __name__

    def _add_resources(self, api, class_kwargs):
        api.add_resource(
            Input,
            self.input_url,
            endpoint='fanvil_input',
            resource_class_kwargs=class_kwargs,
        )
        api.add_resource(
            Lookup,
            self.lookup_url,
            endpoint='fanvil_lookup',
            resource_class_kwargs=class_kwargs,
        )
