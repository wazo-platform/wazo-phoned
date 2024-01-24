# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugin_helpers.client.http import ClientInput, ClientLookup, ClientMenu


class Menu(ClientMenu):
    content_type = 'text/xml; charset=utf-8'
    template = 'cisco_menu.jinja'


class Input(ClientInput):
    content_type = 'text/xml; charset=utf-8'
    template = 'cisco_input.jinja'


class Lookup(ClientLookup):
    content_type = 'text/xml; charset=utf-8'
    template = 'cisco_results.jinja'
