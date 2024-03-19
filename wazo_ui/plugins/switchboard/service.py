# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class SwitchboardService(BaseConfdService):
    resource_confd = 'switchboards'

    def __init__(self, confd_client):
        self._confd = confd_client

    def create(self, switchboard):
        switchboard_created = super().create(switchboard)
        switchboard['uuid'] = switchboard_created['uuid']
        self._confd.switchboards(switchboard).update_user_members(
            switchboard['members']['users']
        )

    def update(self, switchboard):
        super().update(switchboard)
        self._confd.switchboards(switchboard).update_user_members(
            switchboard['members']['users']
        )
        self._confd.switchboards(switchboard).update_fallbacks(switchboard['fallbacks'])

    def get_music_on_hold(self, name):
        results = self._confd.moh.list(name=name)
        for result in results['items']:
            return result
