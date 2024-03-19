# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.extension import BaseConfdExtensionService


class IncallService(BaseConfdExtensionService):
    resource_confd = 'incalls'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_first_incall_context(self, name=None):
        result = self._confd.contexts.list(
            type='incall', name=name, limit=1, direction='asc', order='id'
        )
        for context in result['items']:
            return context

    def get_context(self, context):
        result = self._confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def update(self, incall):
        super().update(incall)
        self._update_schedules_relations(incall)

    def _update_schedules_relations(self, incall):
        schedules = incall.get('schedules')
        if schedules:
            existing_incall = self._confd.incalls.get(incall)
            if existing_incall['schedules']:
                schedule_id = existing_incall['schedules'][0]['id']
                self._confd.incalls(incall).remove_schedule(schedule_id)

            if schedules[0].get('id'):
                self._confd.incalls(incall).add_schedule(schedules[0])

    def list_sound(self):
        return self._confd.sounds.list()
