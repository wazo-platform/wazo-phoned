# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import patch

import pytest

from wazo_phoned.http_server import HTTPServer


@pytest.fixture
def http_server():
    config = {
        'rest_api': {
            'http': {'enabled': True, 'listen': '127.0.0.1', 'port': 9498},
            'https': {'enabled': False},
            'min_threads': 1,
            'max_threads': 1,
            'cors': {'enabled': False},
        },
        'enabled_plugins': [],
        'auth': {},
    }
    return HTTPServer(config)


@patch('wazo_phoned.http_server.cherrypy')
def test_stop_before_run_does_not_raise_and_sets_the_tombstone(cherrypy, http_server):
    http_server.stop()

    assert http_server._stopped.is_set()


@patch('wazo_phoned.http_server.ServerAdapter')
@patch('wazo_phoned.http_server.wsgi')
@patch('wazo_phoned.http_server.cherrypy')
def test_run_after_stop_does_not_start_the_engine(
    cherrypy, wsgi, server_adapter, http_server
):
    http_server.stop()
    http_server.run()

    cherrypy.engine.start.assert_not_called()


@patch('wazo_phoned.http_server.ServerAdapter')
@patch('wazo_phoned.http_server.wsgi')
@patch('wazo_phoned.http_server.cherrypy')
def test_stop_after_run_exits_the_engine(cherrypy, wsgi, server_adapter, http_server):
    http_server.run()
    http_server.stop()

    cherrypy.engine.exit.assert_called_once_with()
