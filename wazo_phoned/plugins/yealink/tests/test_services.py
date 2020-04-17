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
        self.confd.users.get.return_value = {'lines': [{'name': 'line-123'}]}
        self.service.notify_dnd('123', True)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=DNDOn',
                ]
            }
        )

    def test_dnd_notify_disable(self):
        self.confd.users.get.return_value = {'lines': [{'name': 'line-123'}]}
        self.service.notify_dnd('123', False)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=DNDOff',
                ]
            }
        )

    def test_dnd_notify_errors(self):
        http_error = HTTPError()
        http_error.response = MagicMock()
        http_error.response.status_code = 404
        self.confd.users.get.side_effect = http_error
        assert_that(
            calling(self.service.notify_dnd).with_args('123', True),
            raises(NoSuchUser),
        )
        http_error.response.status_code = 500
        assert_that(
            calling(self.service.notify_dnd).with_args('123', True),
            raises(HTTPError),
        )

    def test_dnd_update_enable(self):
        self.service.update_dnd('123', True)
        self.confd.users('123').update_service.assert_called_once_with('dnd', {'enabled': True})

    def test_dnd_update_disable(self):
        self.service.update_dnd('123', False)
        self.confd.users('123').update_service.assert_called_once_with('dnd', {'enabled': False})

    def test_forward_unconditional_notify_enable(self):
        self.confd.users.get.return_value = {'lines': [{'name': 'line-123'}]}
        self.service.notify_forward_unconditional('123', '1002', True)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=AlwaysFwdOn=1002',
                ]
            }
        )

    def test_forward_unconditional_notify_disable(self):
        self.confd.users.get.return_value = {'lines': [{'name': 'line-123'}]}
        self.service.notify_forward_unconditional('123', '1002', False)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=AlwaysFwdOff',
                ]
            }
        )

    def test_forward_unconditional_notify_errors(self):
        http_error = HTTPError()
        http_error.response = MagicMock()
        http_error.response.status_code = 404
        self.confd.users.get.side_effect = http_error
        assert_that(
            calling(self.service.notify_forward_unconditional).with_args('123', '1002', True),
            raises(NoSuchUser),
        )
        http_error.response.status_code = 500
        assert_that(
            calling(self.service.notify_forward_unconditional).with_args('123', '1002', True),
            raises(HTTPError),
        )

    def test_forward_unconditional_enable(self):
        self.service.update_forward_unconditional('123', '1002', True)
        self.confd.users('123').update_forward.assert_called_once_with(
            'unconditional', {'destination': '1002', 'enabled': True}
        )

    def test_forward_unconditional_disable(self):
        self.service.update_forward_unconditional('123', '1002', False)
        self.confd.users('123').update_forward.assert_called_once_with(
            'unconditional', {'destination': '1002', 'enabled': False}
        )

    def test_forward_busy_notify_enable(self):
        self.confd.users.get.return_value = {'lines': [{'name': 'line-123'}]}
        self.service.notify_forward_busy('123', '1002', True)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=BusyFwdOn=1002',
                ]
            }
        )

    def test_forward_busy_notify_disable(self):
        self.confd.users.get.return_value = {'lines': [{'name': 'line-123'}]}
        self.service.notify_forward_busy('123', '1002', False)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=BusyFwdOff',
                ]
            }
        )

    def test_forward_busy_notify_errors(self):
        http_error = HTTPError()
        http_error.response = MagicMock()
        http_error.response.status_code = 404
        self.confd.users.get.side_effect = http_error
        assert_that(
            calling(self.service.notify_forward_busy).with_args('123', '1002', True),
            raises(NoSuchUser),
        )
        http_error.response.status_code = 500
        assert_that(
            calling(self.service.notify_forward_busy).with_args('123', '1002', True),
            raises(HTTPError),
        )

    def test_forward_busy_enable(self):
        self.service.update_forward_busy('123', '1002', True)
        self.confd.users('123').update_forward.assert_called_once_with(
            'busy', {'destination': '1002', 'enabled': True}
        )

    def test_forward_busy_disable(self):
        self.service.update_forward_busy('123', '1002', False)
        self.confd.users('123').update_forward.assert_called_once_with(
            'busy', {'destination': '1002', 'enabled': False}
        )

    def test_forward_noanswer_notify_enable(self):
        self.confd.users.get.return_value = {'lines': [{'name': 'line-123'}]}
        self.service.notify_forward_noanswer('123', '1002', True)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=NoAnswFwdOn=1002',
                ]
            }
        )

    def test_forward_noanswer_notify_disable(self):
        self.confd.users.get.return_value = {'lines': [{'name': 'line-123'}]}
        self.service.notify_forward_noanswer('123', '1002', False)
        self.amid.action.assert_called_once_with(
            'PJSIPNotify',
            {
                'Endpoint': 'line-123',
                'Variable': [
                    'Content-Type=message/sipfrag',
                    'Event=ACTION-URI',
                    'Content=key=NoAnswFwdOff',
                ]
            }
        )

    def test_forward_noanswer_notify_errors(self):
        http_error = HTTPError()
        http_error.response = MagicMock()
        http_error.response.status_code = 404
        self.confd.users.get.side_effect = http_error
        assert_that(
            calling(self.service.notify_forward_noanswer).with_args('123', '1002', True),
            raises(NoSuchUser),
        )
        http_error.response.status_code = 500
        assert_that(
            calling(self.service.notify_forward_noanswer).with_args('123', '1002', True),
            raises(HTTPError),
        )

    def test_forward_noanswer_enable(self):
        self.service.update_forward_noanswer('123', '1002', True)
        self.confd.users('123').update_forward.assert_called_once_with(
            'noanswer', {'destination': '1002', 'enabled': True}
        )

    def test_forward_noanswer_disable(self):
        self.service.update_forward_noanswer('123', '1002', False)
        self.confd.users('123').update_forward.assert_called_once_with(
            'noanswer', {'destination': '1002', 'enabled': False}
        )
