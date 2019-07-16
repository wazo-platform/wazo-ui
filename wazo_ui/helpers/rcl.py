# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session
from requests.exceptions import HTTPError

from wazo_ui.helpers.client import confd_client, wazo_global_auth_client


def refresh_rcl():
    session['rcl'] = get_rcl(session['user']['tenant_uuid'])


def refresh_instance_tenants():
    tenants = wazo_global_auth_client.tenants.list()['items']
    session['instance_tenants'] = tenants
    session['working_instance_tenant_uuid'] = tenants[0]['uuid'] if len(tenants) else None


def get_rcl(tenant_uuid):
    location = _find_location(tenant_uuid)
    if location:
        return Location(location)

    return NoRCL({})


def _find_location(tenant_uuid):
    return _except_404(confd_client.locations.get, tenant_uuid)


def _except_404(callback, *callback_args):
    try:
        return callback(*callback_args)
    except HTTPError as error:
        if error.response.status_code == 404:
            return None
        raise


class RCL:

    def __init__(self, attributes):
        self.type = self.__class__.__name__
        self._attributes = attributes

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d

    def __getattr__(self, item):
        return self._attributes[item]

    def get_children_uuid_tenants(self):
        return []


class Location(RCL):
    pass


class NoRCL(RCL):
    pass
