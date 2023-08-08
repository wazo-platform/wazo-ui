# Copyright 2021-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session
from wazo_dird_client import Client as DirdClient


class _Service:
    def __init__(self, dird_client):
        self._dird: DirdClient = dird_client

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
            tenant_uuid=tenant_uuid,
        )

    def get(self, id: str):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.get(
            phonebook_uuid=id,
            tenant_uuid=tenant_uuid,
        )

    def create(self, data: dict):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.create(
            phonebook_body=data,
            tenant_uuid=tenant_uuid,
        )

    def update(self, data: dict):
        uuid = data.pop('uuid', None)
        assert uuid, f"data={data}"
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.edit(
            phonebook_uuid=uuid,
            phonebook_body=data,
            tenant_uuid=tenant_uuid,
        )

    def delete(self, id: str):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.delete(
            phonebook_uuid=id,
            tenant_uuid=tenant_uuid,
        )


class ManagePhonebookService(_Service):
    def list_phonebook(self):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.list(
            tenant_uuid=tenant_uuid,
        )

    def create_contact(self, contact: dict):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.create_contact(
            phonebook_uuid=contact['phonebook_uuid'],
            contact_body=contact,
            tenant_uuid=tenant_uuid,
        )

    def delete_contact(self, phonebook_uuid: str, contact_uuid: str):
        tenant, tenant_uuid = self._get_tenant()
        self._dird.phonebook.delete_contact(
            phonebook_uuid=phonebook_uuid,
            contact_uuid=contact_uuid,
            tenant_uuid=tenant_uuid,
        )

    def list_contacts(self, phonebook_uuid: str):
        tenant, tenant_uuid = self._get_tenant()
        return self._dird.phonebook.list_contacts(
            tenant_uuid=tenant_uuid,
            phonebook_uuid=phonebook_uuid,
        )
