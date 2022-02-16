# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.extension import BaseConfdService


class SkillRuleService(BaseConfdService):
    resource_confd = 'queue_skill_rules'

    def __init__(self, confd_client):
        self._confd = confd_client
