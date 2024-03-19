# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class OutcallService(BaseConfdService):
    resource_confd = 'outcalls'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_first_outcall_context(self):
        result = self._confd.contexts.list(
            type='outcall', limit=1, direction='asc', order='id'
        )
        for context in result['items']:
            return context

    def get_context(self, context):
        result = self._confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def get_trunk(self, trunk_id):
        return self._confd.trunks.get(trunk_id)

    def create(self, outcall):
        outcall['id'] = super().create(outcall)['id']
        self._update_trunks_relations(outcall)
        self._update_extensions_relations(outcall)
        self._update_schedules_relations(outcall)

    def update(self, outcall):
        super().update(outcall)
        self._update_trunks_relations(outcall)
        self._update_extensions_relations(outcall)
        self._update_schedules_relations(outcall)
        self._update_callpermissions_relations(outcall)

    def _update_trunks_relations(self, outcall):
        if outcall.get('trunks'):
            self._confd.outcalls(outcall['id']).update_trunks(outcall['trunks'])

    def _update_extensions_relations(self, outcall):
        extensions = outcall.get('extensions', [])
        extension_ids = {e.get('id') for e in extensions}
        existing_extensions = self._confd.outcalls.get(outcall['id'])['extensions']
        existing_extension_ids = {e['id'] for e in existing_extensions}
        extension_ids_to_remove = existing_extension_ids - extension_ids

        for extension in extensions:
            if extension.get('id'):
                self._update_or_associate_extension(outcall, extension)
            else:
                self._create_or_associate_extension(outcall, extension)

        self._delete_extension_and_associations(outcall, extension_ids_to_remove)
        self._confd.outcalls.update(outcall)

    def _delete_extension_and_associations(self, outcall, extension_ids_to_remove):
        for id_to_remove in extension_ids_to_remove:
            self._confd.outcalls(outcall).remove_extension(id_to_remove)
            self._confd.extensions.delete(id_to_remove)

    def _create_or_associate_extension(self, outcall, extension):
        existing_extension = self._get_first_existing_extension(extension)

        if not existing_extension:
            extension['id'] = self._confd.extensions.create(extension)['id']
        else:
            extension['id'] = existing_extension['id']

        self._add_or_update_extension_relation(outcall, extension)

    def _get_first_existing_extension(self, extension):
        if extension['exten'] is None:
            return None
        items = self._confd.extensions.list(
            exten=extension['exten'], context=extension['context']
        )['items']
        return items[0] if items else None

    def _update_or_associate_extension(self, outcall, extension):
        self._confd.extensions.update(extension)
        self._add_or_update_extension_relation(outcall, extension)

    def _add_or_update_extension_relation(self, outcall, extension):
        self._confd.outcalls(outcall).add_extension(
            extension,
            prefix=extension['prefix'],
            external_prefix=extension['external_prefix'],
            strip_digits=extension['strip_digits'],
            caller_id=extension['caller_id'],
        )

    def _update_schedules_relations(self, outcall):
        schedules = outcall.get('schedules')
        if schedules:
            existing_outcall = self._confd.outcalls.get(outcall)
            if existing_outcall['schedules']:
                schedule_id = existing_outcall['schedules'][0]['id']
                self._confd.outcalls(outcall).remove_schedule(schedule_id)

            if schedules[0].get('id'):
                self._confd.outcalls(outcall).add_schedule(schedules[0])

    def _update_callpermissions_relations(self, outcall):
        call_permissions = outcall.get('call_permissions')
        existing_resource = self._confd.outcalls.get(outcall)
        if existing_resource and existing_resource.get('call_permissions'):
            for existing_call_permission in existing_resource['call_permissions']:
                self._confd.outcalls(outcall).remove_call_permission(
                    existing_call_permission['id']
                )

        if call_permissions:
            for call_permission in call_permissions:
                self._confd.outcalls(outcall).add_call_permission(call_permission['id'])
