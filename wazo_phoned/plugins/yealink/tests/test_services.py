# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from hamcrest import (
    assert_that,
    calling,
    raises,
)
from requests.exceptions import HTTPError
from unittest.mock import MagicMock

from wazo_phoned.plugin_helpers.client.exceptions import NoSuchUser
from ..services import YealinkService


class TestServices(unittest.TestCase):
    def setUp(self):
        self.amid = MagicMock()
        self.confd = MagicMock()
        self.service = YealinkService(self.amid, self.confd)

    def test_dnd_notify_enable(self):
        self.confd.users.get.return_value = {
            'lines': [{'endpoint_sip': {'name': 'line-123'}}]
        }
        self.service.notify_dnd('123', True)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=DNDOn',
                ],
            },
        )

    def test_dnd_notify_disable(self):
        self.confd.users.get.return_value = {
            'lines': [{'endpoint_sip': {'name': 'line-123'}}]
        }
        self.service.notify_dnd('123', False)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=DNDOff',
                ],
            },
        )

    def test_dnd_notify_no_sip_endpoint(self):
        self.confd.users.get.return_value = {'lines': [{'endpoint_sip': None}]}
        self.service.notify_dnd('123', False)
        self.amid.action.assert_not_called()

    def test_dnd_notify_errors(self):
        http_error = HTTPError()
        http_error.response = MagicMock()
        http_error.response.status_code = 404
        self.confd.users.get.side_effect = http_error
        assert_that(
            calling(self.service.notify_dnd).with_args('123', True), raises(NoSuchUser),
        )
        http_error.response.status_code = 500
        assert_that(
            calling(self.service.notify_dnd).with_args('123', True), raises(HTTPError),
        )

    def test_dnd_update_enable(self):
        self.service.update_dnd('123', True)
        self.confd.users('123').update_service.assert_called_once_with(
            'dnd', {'enabled': True}
        )

    def test_dnd_update_disable(self):
        self.service.update_dnd('123', False)
        self.confd.users('123').update_service.assert_called_once_with(
            'dnd', {'enabled': False}
        )
