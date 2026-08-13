# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import patch

import pytest

from wazo_ui.http_server import Server


@pytest.fixture
def server():
    config = {
        'http': {
            'listen': '127.0.0.1',
            'port': 9296,
            'certificate': None,
            'private_key': None,
        },
        'session_lifetime': 300,
        'debug': False,
        'enabled_plugins': [],
    }
    # the other _configure_* helpers hit the filesystem or wazo-auth
    with (
        patch.object(Server, '_configure_login'),
        patch.object(Server, '_configure_menu'),
        patch.object(Server, '_configure_session'),
        patch.object(Server, '_configure_babel'),
    ):
        return Server(config)


def test_stop_before_run_does_not_raise_and_sets_the_tombstone(server):
    server.stop()

    assert server._stopped.is_set()


@patch('wazo_ui.http_server.wsgi')
def test_run_after_stop_does_not_start_the_server(wsgi, server):
    server.stop()
    server.run()

    wsgi.WSGIServer.return_value.start.assert_not_called()


@patch('wazo_ui.http_server.wsgi')
def test_stop_after_run_stops_the_server(wsgi, server):
    server.run()
    server.stop()

    wsgi.WSGIServer.return_value.stop.assert_called_once_with()
