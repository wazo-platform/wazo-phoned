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

    def _device(self, user_uuid, name, destination=''):
        funckey_prefix = self.confd.extensions_features.list(search='phoneprogfunckey')['items'][0]['exten']
        device_extension = self.confd.extensions_features.list(search=name)['items'][0]['exten']
        user_id = self.confd.users.get(user_uuid)['id']
        funckey_args = (user_id, device_extension, destination)
        funckey_pattern = xivo_helpers.fkey_extension(funckey_prefix, funckey_args)

        hint = self.DEVICE_PATTERN.format(funckey_pattern)
        return hint

    def _send(self, device, status):
        self.amid.command('devstate change {} {}'.format(device, self.INUSE if status else self.NOT_INUSE))

    def notify_dnd(self, user_uuid, status):
        device = self._device(user_uuid, 'enablednd')
        self._send(device, status)

    def notify_forward_unconditional(self, user_uuid, destination, status):
        device = self._device(user_uuid, 'fwdunc', destination)
        self._send(device, status)

    def notify_forward_noanswer(self, user_uuid, destination, status):
        device = self._device(user_uuid, 'fwdrna', destination)
        self._send(device, status)

    def notify_forward_busy(self, user_uuid, destination, status):
        device = self._device(user_uuid, 'fwdbusy', destination)
        self._send(device, status)
