# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
import logging

from xivo import xivo_helpers

logger = logging.getLogger(__name__)


class BlfService:

    DEVICE_PATTERN = 'Custom:{}'
    INUSE = 'INUSE'
    NOT_INUSE = 'NOT_INUSE'

    def __init__(self, amid_client, confd_client):
        self.amid = amid_client
        self.confd = confd_client
        self._extension_features = None

    def _device(self, user_id, name, destination=''):
        funckey_prefix = self.search_extension_feature('phoneprogfunckey')
        device_extension = self.search_extension_feature(name)
        funckey_args = (user_id, device_extension, destination)
        funckey_pattern = xivo_helpers.fkey_extension(funckey_prefix, funckey_args)

        hint = self.DEVICE_PATTERN.format(funckey_pattern)
        return hint

    def _send(self, device, status):
        self.amid.command(
            'devstate change {} {}'.format(
                device, self.INUSE if status else self.NOT_INUSE
            )
        )

    def _update_forward(self, user_id, forward_name, destination, status):
        device = self._device(user_id, forward_name, destination)
        self._send(device, status)
        device = self._device(user_id, forward_name)
        self._send(device, status)

    def notify_dnd(self, user_id, status):
        device = self._device(user_id, 'enablednd')
        self._send(device, status)

    def notify_incallfilter(self, user_id, status):
        device = self._device(user_id, 'incallfilter')
        self._send(device, status)

    def notify_forward_unconditional(self, user_id, destination, status):
        self._update_forward(user_id, 'fwdunc', destination, status)

    def notify_forward_noanswer(self, user_id, destination, status):
        self._update_forward(user_id, 'fwdrna', destination, status)

    def notify_forward_busy(self, user_id, destination, status):
        self._update_forward(user_id, 'fwdbusy', destination, status)

    def invalidate_cache(self):
        logger.debug('Invalidating cache')
        self._extension_features = None

    def _list_extensions_features(self):
        if self._extension_features:
            return self._extension_features
        self._extension_features = self.confd.extensions_features.list()['items']
        return self._extension_features

    def search_extension_feature(self, search_type):
        extension_features = self._list_extensions_features()
        return [
            extension
            for extension in extension_features
            if extension['feature'] == search_type
        ][0]['exten']
