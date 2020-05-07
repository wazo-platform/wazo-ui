# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class CallPermissionService(BaseConfdService):

    resource_confd = 'call_permissions'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get(self, resource_id):
        resource = super().get(resource_id)
        resource['users'] = self._build_user_list(resource['users'])
        return resource

    def _build_user_list(self, users):
        result = []
        for user in users:
            result.append({
                'uuid': user['uuid'],
                'firstname': user['firstname'],
                'lastname': user['lastname']
            })
        return result

    def create(self, resource):
        resource_id = super().create(resource)
        self.update_users(resource_id, resource['user_uuids'], [])
        self.update_groups(resource_id, resource['group_ids'], [])
        self.update_outcalls(resource_id, resource['outcall_ids'], [])

    def update(self, resource):
        super().update(resource)
        existing_resource = self.get(resource['id'])
        self.update_users(resource['id'], resource['user_uuids'], existing_resource['users'])
        self.update_groups(resource['id'], resource['group_ids'], existing_resource['groups'])
        self.update_outcalls(resource['id'], resource['outcall_ids'], existing_resource['outcalls'])

    def update_users(self, callpermission_id, user_uuids, existing_user_uuids):
        for existing_user_uuid in existing_user_uuids:
            self._confd.users(existing_user_uuid).remove_call_permission(callpermission_id)
        for user_uuid in user_uuids:
            self._confd.users(user_uuid).add_call_permission(callpermission_id)

    def update_groups(self, callpermission_id, groups_ids, existing_groups_ids):
        for existing_group_id in existing_groups_ids:
            self._confd.groups(existing_group_id).remove_call_permission(callpermission_id)
        for groups_id in groups_ids:
            self._confd.groups(groups_id).add_call_permission(callpermission_id)

    def update_outcalls(self, callpermission_id, outcall_ids, existing_outcall_ids):
        for existing_outcall_id in existing_outcall_ids:
            self._confd.outcalls(existing_outcall_id).remove_call_permission(callpermission_id)
        for outcall_id in outcall_ids:
            self._confd.outcalls(outcall_id).add_call_permission(callpermission_id)
