# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TypedDict

from flask import session
from wazo_dird_client import Client as DirdClient

logger = logging.getLogger(__name__)


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
    def list(
        self,
        limit=None,
        order=None,
        direction=None,
        offset=None,
        search=None,
    ) -> list[dict]:
        tenant, tenant_uuid = self._get_tenant()
        logger.debug('Querying phonebooks(tenant_uuid=%s)', tenant_uuid)
        return self._dird.phonebook.list(
            tenant_uuid=tenant_uuid,
            limit=limit,
            order=order,
            direction=direction,
            offset=offset,
            search=search,
        )

    def get(self, id: str) -> dict:
        tenant, tenant_uuid = self._get_tenant()
        logger.debug('Querying phonebook(tenant_uuid=%s, uuid=%s)', tenant_uuid, id)
        return self._dird.phonebook.get(
            phonebook_uuid=id,
            tenant_uuid=tenant_uuid,
        )

    def create(self, data: dict) -> dict:
        tenant, tenant_uuid = self._get_tenant()
        logger.debug('Creating phonebook(tenant_uuid=%s)', tenant_uuid)
        return self._dird.phonebook.create(
            phonebook_body=data,
            tenant_uuid=tenant_uuid,
        )

    def update(self, data: dict) -> dict:
        uuid = data.pop('uuid', None)
        assert uuid, f"data={data}"
        tenant, tenant_uuid = self._get_tenant()
        logger.debug('Updating phonebook(tenant_uuid=%s, uuid=%s)', tenant_uuid, uuid)
        return self._dird.phonebook.edit(
            phonebook_uuid=uuid,
            phonebook_body=data,
            tenant_uuid=tenant_uuid,
        )

    def delete(self, id: str):
        tenant, tenant_uuid = self._get_tenant()
        logger.debug(
            'Deleting phonebook(tenant_uuid=%s, uuid=%s)',
            tenant_uuid,
            id,
        )
        return self._dird.phonebook.delete(
            phonebook_uuid=id,
            tenant_uuid=tenant_uuid,
        )


@dataclass(frozen=True)
class ContactSelector:
    phonebook_uuid: str
    contact_id: str


class ListContactParams(TypedDict, total=False):
    phonebook_uuid: str


class ManagePhonebookContactsService(_Service):
    def list_phonebook(self) -> list[dict]:
        tenant, tenant_uuid = self._get_tenant()
        logger.debug('Querying phonebooks(tenant_uuid=%s)', tenant_uuid)
        return self._dird.phonebook.list(
            tenant_uuid=tenant_uuid,
        )['items']

    def create(self, contact: dict) -> dict:
        tenant, tenant_uuid = self._get_tenant()
        logger.debug(
            'Creating contact(tenant_uuid=%s, phonebook_uuid=%s)',
            tenant_uuid,
            contact['phonebook_uuid'],
        )
        return self._dird.phonebook.create_contact(
            phonebook_uuid=contact['phonebook_uuid'],
            contact_body=contact,
            tenant_uuid=tenant_uuid,
        )

    def delete(self, id: ContactSelector):
        tenant, tenant_uuid = self._get_tenant()
        logger.debug(
            'Deleting contact(tenant_uuid=%s, phonebook_uuid=%s, contact_id=%s)',
            tenant_uuid,
            id.phonebook_uuid,
            id.contact_id,
        )
        self._dird.phonebook.delete_contact(
            phonebook_uuid=id.phonebook_uuid,
            contact_uuid=id.contact_id,
            tenant_uuid=tenant_uuid,
        )

    def list(self, **kwargs: ListContactParams) -> list[dict]:
        tenant, tenant_uuid = self._get_tenant()
        phonebook_uuid = kwargs.get('phonebook_uuid')
        logger.debug(
            'Listing contacts(tenant_uuid=%s, phonebook_uuid=%s)',
            tenant_uuid,
            phonebook_uuid,
        )
        return self._dird.phonebook.list_contacts(
            tenant_uuid=tenant_uuid,
            phonebook_uuid=phonebook_uuid,
        )['items']

    def get(self, id: ContactSelector) -> dict:
        tenant, tenant_uuid = self._get_tenant()
        logger.debug(
            'Getting contact(tenant_uuid=%s, phonebook_uuid=%s, contact_id=%s)',
            tenant_uuid,
            id.phonebook_uuid,
            id.contact_id,
        )
        return self._dird.phonebook.get_contact(
            tenant_uuid=tenant_uuid,
            phonebook_uuid=id.phonebook_uuid,
            contact_uuid=id.contact_id,
        )

    def update(self, data: dict) -> dict:
        uuid = data.pop('id', None)
        phonebook_uuid = data.pop('phonebook_uuid')
        assert (
            uuid and phonebook_uuid
        ), f"data={data}, uuid=­{uuid}, phonebook_uuid={phonebook_uuid}"
        tenant, tenant_uuid = self._get_tenant()
        logger.debug(
            'Updating contact(tenant_uuid=%s, phonebook_uuid=%s, contact_id=%s)',
            tenant_uuid,
            phonebook_uuid,
            uuid,
        )
        return self._dird.phonebook.edit_contact(
            contact_uuid=uuid,
            phonebook_uuid=phonebook_uuid,
            contact_body=data,
            tenant_uuid=tenant_uuid,
        )
