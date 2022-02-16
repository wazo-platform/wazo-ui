# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
        self.update_users(
            resource['id'],
            resource['user_uuids'],
            self._extract_ids(existing_resource['users'], 'uuid'),
        )
        self.update_groups(
            resource['id'],
            resource['group_ids'],
            self._extract_ids(existing_resource['groups'], 'id'),
        )
        self.update_outcalls(
            resource['id'],
            resource['outcall_ids'],
            self._extract_ids(existing_resource['outcalls'], 'id'),
        )

    def update_users(self, callpermission_id, user_uuids, existing_user_uuids):
        add, remove = self.find_add_and_remove(user_uuids, existing_user_uuids)
        for existing_user_uuid in remove:
            self._confd.users(existing_user_uuid).remove_call_permission(callpermission_id)
        for user_uuid in add:
            self._confd.users(user_uuid).add_call_permission(callpermission_id)

    def update_groups(self, callpermission_id, group_ids, existing_group_ids):
        add, remove = self.find_add_and_remove(group_ids, existing_group_ids)
        for existing_group_id in remove:
            self._confd.groups(existing_group_id).remove_call_permission(callpermission_id)
        for groups_id in add:
            self._confd.groups(groups_id).add_call_permission(callpermission_id)

    def update_outcalls(self, callpermission_id, outcall_ids, existing_outcall_ids):
        add, remove = self.find_add_and_remove(outcall_ids, existing_outcall_ids)
        for existing_outcall_id in remove:
            self._confd.outcalls(existing_outcall_id).remove_call_permission(callpermission_id)
        for outcall_id in add:
            self._confd.outcalls(outcall_id).add_call_permission(callpermission_id)

    def find_add_and_remove(self, new, existing):
        new_set = set(new or [])
        existing_set = set(existing or [])
        remove = list(existing_set - new_set)
        add = list(new_set - existing_set)
        return add, remove

    @staticmethod
    def _extract_ids(resources, id_field):
        return [resource[id_field] for resource in resources]
