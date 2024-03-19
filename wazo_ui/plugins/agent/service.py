# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.extension import BaseConfdService


class AgentService(BaseConfdService):
    resource_confd = 'agents'

    def __init__(self, confd_client):
        self._confd = confd_client

    def update(self, resource):
        super().update(resource)
        existing_agent = self._confd.agents.get(resource)

        self._update_skills(existing_agent, resource.get('skills'))

    def _update_skills(self, existing_agent, skills):
        # Remove old
        for skill in existing_agent['skills']:
            self._confd.agents.relations(existing_agent['id']).remove_skill(skill['id'])

        # Add new
        for skill in skills:
            self._confd.agents.relations(existing_agent['id']).add_skill(
                skill['skill_id'], **{'skill_weight': skill['skill_weight']}
            )
