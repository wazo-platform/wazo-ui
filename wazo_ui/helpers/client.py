# Copyright 2018 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import g, session
from flask_login import current_user
from werkzeug.local import LocalProxy

from wazo_confd_client import Client as ConfdClient
from wazo_auth_client import Client as AuthClient
from wazo_ui.http_server import app


def wazo_engine_config_client():
    base_config = current_user.get_instance_config()
    base_config['verify_certificate'] = False
    return base_config


def get_auth_client_for_authentication(username, password):
    config = app.config['auth']
    config['username'] = username
    config['password'] = password
    return AuthClient(**config)


def get_wazo_auth_client_from_config(**config):
    client = AuthClient(
        verify_certificate=False,
        prefix='/api/auth',
        **config
    )
    return client


def get_auth_client():
    client = g.get('wazo_auth_client')
    if not client:
        client = g.wazo_auth_client = AuthClient(**app.config['auth'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    return client


auth_client = LocalProxy(get_auth_client)


def get_wazo_auth_client():
    client = g.get('wazo_auth_client')
    if not client:
        client = g.wazo_auth_client = AuthClient(
            prefix='/api/auth',
            **wazo_engine_config_client()
        )
    add_tenant_to(client)

    return client


wazo_auth_client = LocalProxy(get_wazo_auth_client)


def get_global_wazo_auth_client():
    client = g.get('wazo_global_auth_client')
    if not client:
        client = g.wazo_auth_client = AuthClient(
            prefix='/api/auth',
            **wazo_engine_config_client()
        )

    return client


wazo_global_auth_client = LocalProxy(get_global_wazo_auth_client)


def get_confd_client():
    client = g.get('wazo_confd_client')
    if not client:
        client = g.wazo_confd_client = ConfdClient(**app.config['confd'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    return client


confd_client = LocalProxy(get_confd_client)

def add_tenant_to(client):
    if 'working_instance_tenant_uuid' in session and session['working_instance_tenant_uuid']:
        client.set_tenant(session['working_instance_tenant_uuid'])
