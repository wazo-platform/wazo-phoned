# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugin_helpers.client.http import ClientLookup


class Lookup(ClientLookup):
    MAX_ITEM_PER_PAGE = 8
    content_type = 'text/xml; charset=utf-8'
    template = 'thomson_results.jinja'
