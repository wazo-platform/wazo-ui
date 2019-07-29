# Copyright 2019 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session

from wazo_ui.core.client import engine_clients


def refresh_instance_tenants():
    tenants = engine_clients['wazo_auth'].tenants.list()['items']
    session['instance_tenants'] = tenants
    session['working_instance_tenant_uuid'] = tenants[0]['uuid'] if len(tenants) else None
