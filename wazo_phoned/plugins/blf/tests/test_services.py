# Copyright 2020-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import MagicMock, call

from xivo import xivo_helpers

from ..services import BlfService


class TestServices(unittest.TestCase):
    def setUp(self):
        self.amid = MagicMock()
        self.confd = MagicMock()
        self.confd.extensions_features.list.return_value = {
            'items': [
                {'feature': 'phoneprogfunckey', 'exten': '_*735.'},
                {'feature': 'enablednd', 'exten': '*25'},
                {'feature': 'fwdunc', 'exten': '_*21.'},
                {'feature': 'fwdrna', 'exten': '_*22.'},
                {'feature': 'fwdbusy', 'exten': '_*23.'},
                {'feature': 'incallfilter', 'exten': '*27'},
            ],
        }
        self.service = BlfService(self.amid, self.confd)
        xivo_helpers.fkey_extension = MagicMock()

    def test_dnd_enable(self):
        xivo_helpers.fkey_extension.return_value = '*735123***225'

        self.service.notify_dnd('123', True)
        self.amid.command.assert_called_once_with(
            'devstate change Custom:*735123***225 INUSE'
        )

    def test_dnd_disable(self):
        xivo_helpers.fkey_extension.return_value = '*735123***225'

        self.service.notify_dnd('123', False)
        self.amid.command.assert_called_once_with(
            'devstate change Custom:*735123***225 NOT_INUSE'
        )

    def test_incallfilter_enable(self):
        xivo_helpers.fkey_extension.return_value = '*735123***227'

        self.service.notify_incallfilter('123', True)
        self.amid.command.assert_called_once_with(
            'devstate change Custom:*735123***227 INUSE'
        )

    def test_incallfilter_disable(self):
        xivo_helpers.fkey_extension.return_value = '*735123***227'

        self.service.notify_incallfilter('123', False)
        self.amid.command.assert_called_once_with(
            'devstate change Custom:*735123***227 NOT_INUSE'
        )

    def test_forward_unconditional_enable(self):
        xivo_helpers.fkey_extension.side_effect = [
            '*735123***221*1002',
            '*735123***221',
        ]

        self.service.notify_forward_unconditional('123', '1002', True)
        self.amid.command.assert_has_calls(
            [
                call('devstate change Custom:*735123***221*1002 INUSE'),
                call('devstate change Custom:*735123***221 INUSE'),
            ]
        )

    def test_forward_unconditional_disable(self):
        xivo_helpers.fkey_extension.side_effect = [
            '*735123***221*1002',
            '*735123***221',
        ]

        self.service.notify_forward_unconditional('123', '1002', False)
        self.amid.command.assert_has_calls(
            [
                call('devstate change Custom:*735123***221*1002 NOT_INUSE'),
                call('devstate change Custom:*735123***221 NOT_INUSE'),
            ]
        )

    def test_forward_busy_enable(self):
        xivo_helpers.fkey_extension.side_effect = [
            '*735123***223*1002',
            '*735123***223',
        ]

        self.service.notify_forward_busy('123', '1002', True)
        self.amid.command.assert_has_calls(
            [
                call('devstate change Custom:*735123***223*1002 INUSE'),
                call('devstate change Custom:*735123***223 INUSE'),
            ]
        )

    def test_forward_busy_disable(self):
        xivo_helpers.fkey_extension.side_effect = [
            '*735123***223*1002',
            '*735123***223',
        ]

        self.service.notify_forward_busy('123', '1002', False)
        self.amid.command.assert_has_calls(
            [
                call('devstate change Custom:*735123***223*1002 NOT_INUSE'),
                call('devstate change Custom:*735123***223 NOT_INUSE'),
            ]
        )

    def test_forward_noanswer_enable(self):
        xivo_helpers.fkey_extension.side_effect = [
            '*735123***222*1002',
            '*735123***222',
        ]

        self.service.notify_forward_noanswer('123', '1002', True)
        self.amid.command.assert_has_calls(
            [
                call('devstate change Custom:*735123***222*1002 INUSE'),
                call('devstate change Custom:*735123***222 INUSE'),
            ]
        )

    def test_forward_noanswer_disable(self):
        xivo_helpers.fkey_extension.side_effect = [
            '*735123***222*1002',
            '*735123***222',
        ]

        self.service.notify_forward_noanswer('123', '1002', False)
        self.amid.command.assert_has_calls(
            [
                call('devstate change Custom:*735123***222*1002 NOT_INUSE'),
                call('devstate change Custom:*735123***222 NOT_INUSE'),
            ]
        )

    def test_extension_feature_is_cached(self):
        xivo_helpers.fkey_extension.return_value = '*735123***225'

        self.service.notify_dnd('123', True)
        self.service.notify_dnd('123', True)
        self.confd.extensions_features.list.assert_called_once()

        self.service.invalidate_cache()
        self.confd.reset_mock()
        self.service.notify_dnd('123', True)
        self.confd.extensions_features.list.assert_called_once()
