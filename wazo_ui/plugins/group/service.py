# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.extension import BaseConfdExtensionService


class GroupService(BaseConfdExtensionService):
    resource_confd = 'groups'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def create(self, resource):
        resource_created = super().create(resource)
        resource['uuid'] = resource_created['uuid']
        del resource['fallbacks']
        self._update_relations(resource)

    def update(self, resource):
        super().update(resource)
        existing_group = self._confd.groups.get(resource)
        self._update_relations(resource, existing_group)

    def _update_relations(self, group, existing_group=None):
        members = group.get('members')
        extensions_members = group.get('extensions_members', [])
        fallbacks = group.get('fallbacks')
        schedules = group.get('schedules')
        call_permissions = group.get('call_permissions')

        if members:
            self._update_members_to_group(group, members)

        if fallbacks:
            self._update_fallbacks_to_group(group, fallbacks)

        if schedules:
            self._update_schedules_to_group(group, schedules, existing_group)

        if call_permissions:
            self._update_callpermissions_relations(
                group, call_permissions, existing_group
            )

        self._update_extensions_members_to_group(group, extensions_members)

    def _update_members_to_group(self, group, members):
        return self._confd.groups.relations(group).update_user_members(
            members.get('users')
        )

    def _update_extensions_members_to_group(self, group, extensions_members):
        context = group.get('extensions')[0]['context']
        for member in extensions_members:
            member['context'] = context
        return self._confd.groups.relations(group).update_extension_members(
            extensions_members
        )

    def _update_fallbacks_to_group(self, group, fallbacks):
        return self._confd.groups.relations(group).update_fallbacks(fallbacks)

    def _update_schedules_to_group(self, group, schedules, existing_group):
        if existing_group and existing_group.get('schedules'):
            schedule_id = existing_group['schedules'][0]['id']
            self._confd.groups(group).remove_schedule(schedule_id)
        if schedules[0].get('id'):
            self._confd.groups(group).add_schedule(schedules[0])

    def _update_callpermissions_relations(
        self, group, call_permissions, existing_group
    ):
        if existing_group and existing_group.get('call_permissions'):
            for existing_call_permission in existing_group['call_permissions']:
                self._confd.groups(group).remove_call_permission(
                    existing_call_permission['id']
                )

        for call_permission in call_permissions:
            self._confd.groups(group).add_call_permission(call_permission['id'])

    def get_first_internal_context(self):
        result = self._confd.contexts.list(
            type='internal', limit=1, direction='asc', order='id'
        )
        for context in result['items']:
            return context

    def get_context(self, context):
        result = self._confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def get_music_on_hold(self, name):
        results = self._confd.moh.list(name=name)
        for result in results['items']:
            return result
