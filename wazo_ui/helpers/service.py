# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from flask_login import current_user
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


class BaseNestboxConfdService:
    resource_confd = None

    def list(self):
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.list()

    def get(self, resource_id):
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.get(resource_id)

    def update(self, resource):
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client.update(resource['uuid'], resource)

    def create(self, resource):
        resource_client = getattr(self._confd, self.resource_confd)
        return resource_client.create(resource)

    def delete(self, resource_id):
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client.delete(resource_id)


class BaseRCLConfdService(BaseNestboxConfdService):

    def list(self):
        return self._list(self_remove=False)

    def listing(self):
        return self._list(self_remove=False)

    def _list(self, self_remove=False):
        resources = super().list()
        if not self_remove:
            return resources

        self_resource = next(
            (resource for resource in resources['items'] if current_user.get_tenant_uuid() == resource['uuid']),
            None
        )
        if self_resource:
            resources['items'].remove(self_resource)
            resources['total'] = resources['total'] - 1
        return resources

    def delete(self, resource_id):
        super().delete(resource_id)
        users = self._auth.tenants.get_users(resource_id)['items']
        for user in users:
            self._auth.users.delete(user['uuid'])
        self._auth.tenants.delete(resource_id)

    def list_credentials(self, tenant_uuid):
        try:
            return self._auth.tenants.get_users(tenant_uuid=tenant_uuid)
        except HTTPError as error:
            if error.response.status_code == 404:
                return {'items': []}
            raise


class BaseAuthService:
    resource_auth = None

    def list(self, limit=None, order=None, direction=None, offset=None, search=None, **kwargs):
        resource_client = getattr(self._auth, self.resource_auth)
        return resource_client.list(search=search,
                                    order=order,
                                    limit=limit,
                                    direction=direction,
                                    offset=offset,
                                    **kwargs)

    def get(self, resource_id):
        resource_client = getattr(self._auth, self.resource_auth)
        return resource_client.get(resource_id)

    def update(self, resource):
        resource_client = getattr(self._auth, self.resource_auth)
        resource_client.edit(resource['uuid'], **resource)

    def create(self, resource):
        resource_client = getattr(self._auth, self.resource_auth)
        return resource_client.new(**resource)

    def delete(self, resource_id):
        resource_client = getattr(self._auth, self.resource_auth)
        resource_client.delete(resource_id)
