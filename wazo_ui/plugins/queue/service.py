# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.extension import BaseConfdExtensionService


class QueueService(BaseConfdExtensionService):
    resource_confd = 'queues'

    def __init__(self, confd_client):
        self._confd = confd_client

    def create(self, resource):
        del resource['wait_time_destination']
        del resource['wait_ratio_destination']
        resource['enabled'] = True
        super().create(resource)

    def update(self, resource):
        super().update(resource)
        existing_queue = self._confd.queues.get(resource)
        self._update_relations(resource, existing_queue)

    def _update_relations(self, queue, existing_queue=None):
        fallbacks = queue.get('fallbacks')
        schedules = queue.get('schedules')
        users = queue.get('members').get('user_ids')
        agents = queue.get('members').get('agent_ids')

        if fallbacks:
            self._update_fallbacks_to_queue(queue, fallbacks)

        self._update_users_to_queue(existing_queue, users)

        self._update_agents_to_queue(existing_queue, agents)

        if schedules:
            self._update_schedules_to_queue(queue, schedules, existing_queue)

    def _update_fallbacks_to_queue(self, queue, fallbacks):
        return self._confd.queues.relations(queue).update_fallbacks(fallbacks)

    def _update_users_to_queue(self, existing_queue, user_ids):
        for existing_user in existing_queue['members']['users']:
            self._confd.queues.relations(existing_queue).remove_user_member(
                existing_user['uuid']
            )

        for user_id in user_ids:
            self._confd.queues.relations(existing_queue).add_user_member(user_id)

    def _update_agents_to_queue(self, existing_queue, agent_ids):
        for existing_agent in existing_queue['members']['agents']:
            self._confd.queues.relations(existing_queue).remove_agent_member(
                existing_agent['id']
            )

        for agent_id in agent_ids:
            self._confd.queues.relations(existing_queue).add_agent_member(agent_id)

    def _update_schedules_to_queue(self, queue, schedules, existing_queue):
        if existing_queue and existing_queue.get('schedules'):
            schedule_id = existing_queue['schedules'][0]['id']
            self._confd.queues(queue).remove_schedule(schedule_id)
        if schedules[0].get('id'):
            self._confd.queues(queue).add_schedule(schedules[0])

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

    def get_fallbacks(self, queue_id):
        return self._confd.queues(queue_id).list_fallbacks()

    def get_music_on_hold(self, name):
        results = self._confd.moh.list(name=name)
        for result in results['items']:
            return result
