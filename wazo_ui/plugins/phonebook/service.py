# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import session


class PhonebookService:

    def __init__(self, dird_client):
        self._dird = dird_client

    def list(self):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.list(tenant=tenant, tenant_uuid=tenant_uuid)

    def get(self, id):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.get(tenant=tenant, phonebook_id=id, tenant_uuid=tenant_uuid)

    def create(self, data):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.create(tenant=tenant, phonebook_body=data, tenant_uuid=tenant_uuid)

    def update(self, data):
        id = data['id']
        data.pop('id', None)
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.edit(tenant=tenant, phonebook_id=id, phonebook_body=data, tenant_uuid=tenant_uuid)

    def delete(self, id):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.delete(tenant=tenant, phonebook_id=id, tenant_uuid=tenant_uuid)

    def _get_tenant(self):
        tenant_uuid = session['working_instance_tenant_uuid']
        tenant = [tenant['name'] for tenant in session['instance_tenants'] if tenant['uuid'] == tenant_uuid][0]
        return (tenant, tenant_uuid)
