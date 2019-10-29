# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import g, session
from flask_login import current_user
from werkzeug.local import LocalProxy

from wazo_amid_client import Client as AmidClient
from wazo_auth_client import Client as AuthClient
from wazo_call_logd_client import Client as CallLogdClient
from wazo_confd_client import Client as ConfdClient
from wazo_dird_client import Client as DirdClient
from wazo_plugind_client import Client as PlugindClient
from wazo_provd_client import Client as ProvdClient
from wazo_webhookd_client import Client as WebhookdClient

from wazo_ui.http_server import app


def get_provd_client():
    client = g.get('wazo_provd_client')
    if not client:
        client = g.wazo_provd_client = ProvdClient(**app.config['provd'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    add_tenant_to(client)
    return client


def get_auth_client():
    client = g.get('wazo_auth_client')
    if not client:
        client = g.wazo_auth_client = AuthClient(**app.config['auth'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    add_tenant_to(client)
    return client


def get_amid_client():
    client = g.get('wazo_amid_client')
    if not client:
        client = g.wazo_amid_client = AmidClient(**app.config['amid'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    add_tenant_to(client)
    return client


def get_call_logd_client():
    client = g.get('wazo_call_logd_client')
    if not client:
        client = g.wazo_call_logd_client = CallLogdClient(**app.config['call-logd'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    add_tenant_to(client)
    return client


def get_webhookd_client():
    client = g.get('wazo_webhookd_client')
    if not client:
        client = g.wazo_webhookd_client = WebhookdClient(**app.config['webhookd'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    add_tenant_to(client)
    return client


def get_plugind_client():
    client = g.get('wazo_plugind_client')
    if not client:
        client = g.wazo_plugind_client = PlugindClient(**app.config['plugind'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    add_tenant_to(client)
    return client


def get_wazo_confd_client():
    client = g.get('wazo_confd_client')
    if not client:
        client = g.wazo_confd_client = ConfdClient(**app.config['confd'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    add_tenant_to(client)
    return client


def get_wazo_dird_client():
    client = g.get('wazo_dird_client')
    if not client:
        client = g.wazo_confd_client = DirdClient(**app.config['dird'])
        client.set_token(current_user.get_id())
        client.set_tenant(current_user.get_tenant_uuid())
    add_tenant_to(client)
    return client


def add_tenant_to(client):
    if 'working_instance_tenant_uuid' in session and session['working_instance_tenant_uuid']:
        client.set_tenant(session['working_instance_tenant_uuid'])


engine_clients = {
    'wazo_auth': LocalProxy(get_auth_client),
    'wazo_confd': LocalProxy(get_wazo_confd_client),
    'wazo_webhookd': LocalProxy(get_webhookd_client),
    'wazo_call_logd': LocalProxy(get_call_logd_client),
    'wazo_amid': LocalProxy(get_amid_client),
    'wazo_provd': LocalProxy(get_provd_client),
    'wazo_plugind': LocalProxy(get_plugind_client),
    'wazo_dird': LocalProxy(get_wazo_dird_client)
}
