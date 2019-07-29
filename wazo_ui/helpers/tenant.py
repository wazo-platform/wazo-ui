# Copyright 2019 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session

from .client import wazo_global_auth_client


def refresh_instance_tenants():
    tenants = wazo_global_auth_client.tenants.list()['items']
    session['instance_tenants'] = tenants
    session['working_instance_tenant_uuid'] = tenants[0]['uuid'] if len(tenants) else None
