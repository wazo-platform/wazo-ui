# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session


class _Service:

    def __init__(self, dird_client):
        self._dird = dird_client

    def _get_tenant(self):
        tenant_uuid = session['working_tenant_uuid']
        for tenant in session['tenants']:
            if tenant['uuid'] == tenant_uuid:
                return (tenant['name'], tenant_uuid)
        raise Exception('Working tenant not found in tenant list')


class PhonebookService(_Service):

    def list(self):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.list(
            tenant=tenant,
            tenant_uuid=tenant_uuid,
        )

    def get(self, id):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.get(
            tenant=tenant,
            phonebook_id=id,
            tenant_uuid=tenant_uuid,
        )

    def create(self, data):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.create(
            tenant=tenant,
            phonebook_body=data,
            tenant_uuid=tenant_uuid,
        )

    def update(self, data):
        id = data['id']
        data.pop('id', None)
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.edit(
            tenant=tenant,
            phonebook_id=id,
            phonebook_body=data,
            tenant_uuid=tenant_uuid,
        )

    def delete(self, id):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.delete(
            tenant=tenant,
            phonebook_id=id,
            tenant_uuid=tenant_uuid,
        )


class ManagePhonebookService(_Service):

    def list_phonebook(self):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.list(
            tenant=tenant,
            tenant_uuid=tenant_uuid,
        )

    def create_contact(self, contact):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.create_contact(
            tenant=tenant,
            phonebook_id=contact['phonebook_id'],
            contact_body=contact,
            tenant_uuid=tenant_uuid,
        )

    def delete_contact(self, phonebook_id, contact_uuid):
        tenant, tenant_uuid = self._get_tenant()
        self._dird.phonebook.delete_contact(
            tenant=tenant,
            phonebook_id=phonebook_id,
            contact_uuid=contact_uuid,
            tenant_uuid=tenant_uuid,
        )

    def list_contacts(self, phonebook_id):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.list_contacts(
            tenant=tenant,
            tenant_uuid=tenant_uuid,
            phonebook_id=phonebook_id,
        )
