# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class LineService(BaseConfdService):
    resource_confd = 'lines'

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

    def get_endpoint_sccp(self, endpoint_id):
        return self._confd.endpoints_sccp.get(endpoint_id)

    def get_endpoint_custom(self, endpoint_id):
        return self._confd.endpoints_custom.get(endpoint_id)

    def get_transport(self, uuid):
        return self._confd.sip_transports.get(uuid)

    def get_sip_template(self, uuid):
        return self._confd.endpoints_sip_templates.get(uuid)

    def create(self, resource):
        resource_created = super().create(resource)
        resource['id'] = resource_created['id']
        if resource.get('endpoint_sip'):
            endpoint_sip = self._confd.endpoints_sip.create(resource['endpoint_sip'])
            self._confd.lines(resource['id']).add_endpoint_sip(endpoint_sip['uuid'])
        if resource.get('endpoint_sccp'):
            endpoint_sccp = self._confd.endpoints_sccp.create(resource['endpoint_sccp'])
            self._confd.lines(resource['id']).add_endpoint_sccp(endpoint_sccp['id'])
        if resource.get('endpoint_custom'):
            endpoint_custom = self._confd.endpoints_custom.create(
                resource['endpoint_custom']
            )
            self._confd.lines(resource['id']).add_endpoint_custom(endpoint_custom['id'])

    def update(self, resource):
        super().update(resource)
        if resource.get('endpoint_sip'):
            self._confd.endpoints_sip.update(resource['endpoint_sip'])
        if resource.get('endpoint_sccp'):
            self._confd.endpoints_sccp.update(resource['endpoint_sccp'])
        if resource.get('endpoint_custom'):
            self._confd.endpoints_custom.update(resource['endpoint_custom'])
