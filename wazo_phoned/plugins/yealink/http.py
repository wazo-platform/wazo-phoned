# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugin_helpers.client.http import ClientLookup


class Lookup(ClientLookup):
    content_type = 'text/xml; charset=utf-8'
    template = 'yealink_results.jinja'
