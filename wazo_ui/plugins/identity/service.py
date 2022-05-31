# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_login import current_user


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


class IdentityService(BaseAuthService):
    resource_auth = 'users'

    def __init__(self, auth_client):
        self._auth = auth_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get(self, resource_id):
        resource = self._auth.users.get(resource_id)
        resource['members'] = {}
        resource['members']['groups'] = self._auth.users.get_groups(resource['uuid'])['items']
        resource['members']['policies'] = self._auth.users.get_policies(resource['uuid'])['items']
        resource['tenant'] = self._auth.tenants.get(resource['tenant_uuid'])
        return resource

    def update(self, resource):
        if resource['emails']:
            self._auth.users.update_emails(resource['uuid'], resource['emails'])
            del resource['emails']
        if resource['password']:
            self._auth.users.set_password(resource['uuid'], resource['password'])
        self._update_groups(resource, resource['members']['groups'])
        self._update_policies(resource, resource['members']['policies'])
        self._auth.users.edit(resource['uuid'], **resource)

    def _update_groups(self, resource, groups):
        groups = groups or []
        existing_groups = self._auth.users.get_groups(resource['uuid'])['items']

        group_uuids = {group.get('uuid') for group in groups}
        existing_group_uuids = {group['uuid'] for group in existing_groups}
        group_uuids_to_remove = existing_group_uuids - group_uuids
        for group_uuid in group_uuids_to_remove:
            self._auth.groups.remove_user(group_uuid, resource['uuid'])

        group_uuids_to_add = group_uuids - existing_group_uuids
        for group_uuid in group_uuids_to_add:
            self._auth.groups.add_user(group_uuid, resource['uuid'])

    def _update_policies(self, resource, policies):
        existing_policies = self._auth.users.get_policies(resource['uuid'])['items']
        if existing_policies:
            for policy in existing_policies:
                self._auth.users.remove_policy(resource['uuid'], policy['uuid'])
        if policies:
            for policy in policies:
                self._auth.users.add_policy(resource['uuid'], policy['uuid'])


class GroupService(BaseAuthService):
    resource_auth = 'groups'

    def __init__(self, auth_client):
        self._auth = auth_client

    def get(self, resource_id):
        resource = self._auth.groups.get(resource_id)
        resource['members'] = {}
        resource['members']['users'] = self._auth.groups.get_users(resource['uuid'])['items']
        resource['members']['policies'] = self._auth.groups.get_policies(resource['uuid'])['items']
        return resource

    def update(self, resource):
        self._update_users(resource, resource['members']['users'])
        self._update_policies(resource, resource['members']['policies'])
        self._auth.groups.edit(resource['uuid'], **resource)

    def _update_users(self, resource, users):
        existing_users = self._auth.groups.get_users(resource['uuid'])['items']
        if existing_users:
            for user in existing_users:
                self._auth.groups.remove_user(resource['uuid'], user['uuid'])
        if users:
            for user in users:
                self._auth.groups.add_user(resource['uuid'], user['uuid'])

    def _update_policies(self, resource, policies):
        existing_policies = self._auth.groups.get_policies(resource['uuid'])['items']
        if existing_policies:
            for policy in existing_policies:
                self._auth.groups.remove_policy(resource['uuid'], policy['uuid'])
        if policies:
            for policy in policies:
                self._auth.groups.add_policy(resource['uuid'], policy['uuid'])


class TenantService(BaseAuthService):
    resource_auth = 'tenants'

    def __init__(self, auth_client):
        self._auth = auth_client

    def list(self):
        tenant_uuid = current_user.get_tenant_uuid()
        tenants = self._auth.tenants.list(tenant_uuid=tenant_uuid, recurse=True)['items']
        tenants = [tenant for tenant in tenants if tenant['name'] != 'master']
        resources = {
            'items': tenants,
            'total': len(tenants),
            'filtered': len(tenants),
        }
        return resources

    def get(self, resource_id):
        resource = self._auth.tenants.get(resource_id)
        resource['members'] = {}
        resource['members']['users'] = self._auth.tenants.get_users(resource['uuid'])['items']
        resource['members']['policies'] = self._auth.tenants.get_policies(resource['uuid'])['items']
        return resource

    def update(self, resource):
        resource = self._update_resource_with_domain_names(resource, resource['domain_names'])
        self._auth.tenants.edit(resource['uuid'], **resource)

    def new(self, resource):
        resource = self._update_resource_with_domain_names(resource, resource['domain_names'])
        self._auth.tenants.new(**resource)

    def _update_resource_with_domain_names(self, resource, domain_names):
        existing_domain_names = self._auth.tenants.get(resource['uuid'])['domain_names']
        new_domain_names = [domain.get('name') for domain in domain_names if domain.get('name')]
        if new_domain_names:
            resource['domain_names'] = new_domain_names
        else:
            resource['domain_names'] = existing_domain_names
        return resource


class PolicyService(BaseAuthService):
    resource_auth = 'policies'

    def __init__(self, auth_client):
        self._auth = auth_client

    def update(self, resource):
        uuid = resource['uuid']
        del resource['uuid']
        self._auth.policies.edit(uuid, **resource)


class LDAPService(BaseAuthService):
    resource_auth = 'ldap_config'

    def __init__(self, auth_client):
        self._auth = auth_client

    def get(self):
        tenant_uuid = current_user.get_tenant_uuid()
        return self._auth.ldap_config.get(tenant_uuid)

    def update(self, resource):
        tenant_uuid = current_user.get_tenant_uuid()
        self._auth.ldap_config.update(resource, tenant_uuid=tenant_uuid)

    def delete(self):
        tenant_uuid = current_user.get_tenant_uuid()
        self._auth.ldap_config.delete(tenant_uuid)
