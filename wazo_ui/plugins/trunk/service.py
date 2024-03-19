# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class TrunkService(BaseConfdService):
    resource_confd = 'trunks'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_context(self, context):
        result = self._confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def get_endpoint_sip(self, endpoint_uuid):
        return self._confd.endpoints_sip.get(endpoint_uuid)

    def get_endpoint_iax(self, endpoint_id):
        return self._confd.endpoints_iax.get(endpoint_id)

    def get_endpoint_custom(self, endpoint_id):
        return self._confd.endpoints_custom.get(endpoint_id)

    def get_register_iax(self, endpoint_iax):
        return self._confd.registers_iax.get(endpoint_iax)

    def get_transport(self, uuid):
        return self._confd.sip_transports.get(uuid)

    def get_sip_template(self, uuid):
        return self._confd.endpoints_sip_templates.get(uuid)

    def create(self, resource):
        resource_created = super().create(resource)
        resource['id'] = resource_created['id']
        if resource.get('endpoint_sip'):
            endpoint_sip = self._confd.endpoints_sip.create(resource['endpoint_sip'])
            self._confd.trunks(resource['id']).add_endpoint_sip(endpoint_sip['uuid'])
        if resource.get('endpoint_iax'):
            endpoint_iax = self._confd.endpoints_iax.create(resource['endpoint_iax'])
            self._confd.trunks(resource['id']).add_endpoint_iax(endpoint_iax['id'])
        if resource.get('register_iax'):
            register_iax = self._confd.registers_iax.create(resource['register_iax'])
            self._confd.trunks(resource['id']).add_register_iax(register_iax)
        if resource.get('endpoint_custom'):
            endpoint_custom = self._confd.endpoints_custom.create(
                resource['endpoint_custom']
            )
            self._confd.trunks(resource['id']).add_endpoint_custom(
                endpoint_custom['id']
            )

    def update(self, resource):
        super().update(resource)
        if resource.get('endpoint_sip'):
            self._confd.endpoints_sip.update(resource['endpoint_sip'])
        if resource.get('endpoint_iax'):
            self._confd.endpoints_iax.update(resource['endpoint_iax'])
            self._update_register_iax(resource)
        if resource.get('endpoint_custom'):
            self._confd.endpoints_custom.update(resource['endpoint_custom'])

    def _update_register_iax(self, resource):
        existing_trunk = self.get(resource['id'])
        if existing_trunk.get('register_iax') and resource.get('register_iax'):
            self._confd.registers_iax.update(resource['register_iax'])
        elif not existing_trunk.get('register_iax') and resource.get('register_iax'):
            register_iax = self._confd.registers_iax.create(resource['register_iax'])
            self._confd.trunks(resource).add_register_iax(register_iax)
        elif existing_trunk.get('register_iax') and not resource.get('register_iax'):
            self._confd.registers_iax.delete(existing_trunk['register_iax']['id'])
