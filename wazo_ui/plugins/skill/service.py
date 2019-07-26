# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.extension import BaseConfdService


class SkillService(BaseConfdService):
    resource_confd = 'agent_skills'

    def __init__(self, confd_client):
        self._confd = confd_client
