# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .resource import (
    Menu,
    Input,
    Lookup,
    LookupGigaset,
)


class Plugin:

    menu_url = '/directories/menu/<profile>/<vendor>'
    input_url = '/directories/input/<profile>/<vendor>'
    lookup_url = '/directories/lookup/<profile>/<vendor>'
    lookup_gigaset_url = '/directories/lookup/<profile>/gigaset/<xivo_user_uuid>'

    def load(self, dependencies):
        api = dependencies['api']
        dird_config = dependencies['config']['dird']
        dird_host = dird_config['host']
        dird_port = dird_config['port']
        dird_verify_certificate = dird_config.get('verify_certificate', True)

        Menu.configure(dird_host, dird_port, dird_verify_certificate)
        Input.configure(dird_host, dird_port, dird_verify_certificate)
        Lookup.configure(dird_host, dird_port, dird_verify_certificate)
        LookupGigaset.configure(dird_host, dird_port, dird_verify_certificate)
        api.add_resource(Menu, self.menu_url)
        api.add_resource(Input, self.input_url)
        api.add_resource(Lookup, self.lookup_url)
        api.add_resource(LookupGigaset, self.lookup_gigaset_url)
