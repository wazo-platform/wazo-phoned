# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from requests.exceptions import RequestException
from wazo_phoned.plugin_helpers.client.exceptions import (
    NoSuchDevice,
    NowhereToRouteEndpoint,
    NoSuchEndpoint,
)

logger = logging.getLogger(__name__)


class EndpointService:
    def __init__(self, phone_plugins, confd_client):
        self.phone_plugins = phone_plugins
        self.confd = confd_client

    def hold(self, endpoint_name):
        plugin = self.route_to_plugin(endpoint_name)
        if plugin:
            if hasattr(plugin, 'service'):
                if hasattr(plugin.service, 'hold_call'):
                    plugin.service.hold_call(endpoint_name)
        else:
            logger.debug('No plugin found for endpoint %s', endpoint_name)
            raise NowhereToRouteEndpoint(endpoint_name)

    def unhold(self, endpoint_name):
        plugin = self.route_to_plugin(endpoint_name)
        if plugin:
            if hasattr(plugin, 'service'):
                if hasattr(plugin.service, 'unhold_call'):
                    plugin.service.unhold_call(endpoint_name)
        else:
            logger.debug('No plugin found for endpoint %s', endpoint_name)
            raise NowhereToRouteEndpoint(endpoint_name)

    def route_to_plugin(self, endpoint_name):
        vendor = self._find_endpoint_vendor(endpoint_name)
        if vendor:
            return self._match_vendor_against_plugin(vendor)

    def _find_endpoint_vendor(self, endpoint_name):
        results = self.confd.lines.list(search=endpoint_name, recurse=True)['items']
        if results:
            device_id = results[0]['device_id']
            try:
                device = self.confd.devices.get(device_id)
            except RequestException as e:
                response = getattr(e, 'response', None)
                status_code = getattr(response, 'status_code', None)
                if status_code == 404:
                    raise NoSuchDevice(device_id)
                raise
            return device['vendor']
        raise NoSuchEndpoint(endpoint_name)

    def _match_vendor_against_plugin(self, vendor):
        for plugin in self.phone_plugins:
            logger.debug('Matching %s against phone plugin %s', vendor, plugin)
            if hasattr(plugin, 'match_vendor'):
                if plugin.match_vendor(vendor):
                    return plugin
        return
