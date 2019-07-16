# Copyright 2018 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_login import current_user
from requests.exceptions import HTTPError

from .client import get_wazo_auth_client_from_config


def get_wazo_tenant_from_wazo_auth(wazo_auth_client, wazo_tenant_uuid):
    try:
        return wazo_auth_client.tenants.get(wazo_tenant_uuid)
    except HTTPError:
        pass


def get_wazo_auth_client_from_credential(credential):
    wazo_auth_config = {
        'host': credential['instance']['remote_host'],
        'port': credential['instance']['https_port'],
        'username': credential['username'],
        'password': credential['password'],
    }
    wazo_auth_client = get_wazo_auth_client_from_config(**wazo_auth_config)
    try:
        token = wazo_auth_client.token.new('wazo_user', expiration=60 * 60 * 12)['token']
    except HTTPError:
        token = wazo_auth_client.token.new('xivo_admin', expiration=60 * 60 * 12)['token']
    wazo_auth_client.set_token(token)
    return wazo_auth_client


def get_wazo_auth_client_from_instance(instance):
    wazo_auth_config = {
        'host': instance['remote_host'],
        'port': instance['https_port'],
        'username': instance['username'],
        'password': instance['password'],
    }
    wazo_auth_client = get_wazo_auth_client_from_config(**wazo_auth_config)
    try:
        token = wazo_auth_client.token.new('wazo_user', expiration=60 * 60 * 12)['token']
    except HTTPError:
        token = wazo_auth_client.token.new('xivo_admin', expiration=60 * 60 * 12)['token']
    wazo_auth_client.set_token(token)
    return wazo_auth_client


def wazo_connect_from_credential(credential, wazo_tenant_uuid):
    wazo_auth_config = {
        'host': credential['instance']['remote_host'],
        'port': credential['instance']['https_port'],
        'username': credential['username'],
        'password': credential['password'],
    }
    wazo_auth_client = get_wazo_auth_client_from_config(**wazo_auth_config)
    try:
        token = wazo_auth_client.token.new('wazo_user', expiration=60 * 60 * 12)['token']
    except HTTPError:
        token = wazo_auth_client.token.new('xivo_admin', expiration=60 * 60 * 12)['token']

    instance_config = {
        'host': credential['instance']['remote_host'],
        'port': credential['instance']['https_port'],
        'tenant_uuid': credential['instance']['tenant_uuid'],
        'uuid': credential['instance']['uuid'],
        'name': credential['instance']['name'],
        'service_id': credential['instance']['service_id'],
        'token': token,
    }

    wazo_auth_client.set_token(token)
    wazo_tenant = get_wazo_tenant_from_wazo_auth(wazo_auth_client, wazo_tenant_uuid)

    current_user.set_instance(instance_config, wazo_tenant)


def wazo_connect_from_instance(instance):
    wazo_auth_config = {
        'host': instance['remote_host'],
        'port': instance['https_port'],
        'username': instance['username'],
        'password': instance['password'],
    }
    wazo_auth_client = get_wazo_auth_client_from_config(**wazo_auth_config)
    try:
        token = wazo_auth_client.token.new('wazo_user', expiration=60 * 60 * 12)['token']
    except HTTPError:
        token = wazo_auth_client.token.new('xivo_admin', expiration=60 * 60 * 12)['token']

    instance_config = {
        'host': instance['remote_host'],
        'port': instance['https_port'],
        'tenant_uuid': instance['tenant_uuid'],
        'uuid': instance['uuid'],
        'name': instance['name'],
        'service_id': instance['service_id'],
        'token': token,
    }

    wazo_tenant = None
    current_user.set_instance(instance_config, wazo_tenant)


def wazo_disconnect():
    current_user.reset_instance()
