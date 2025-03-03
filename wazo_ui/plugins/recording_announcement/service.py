# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from wazo_ui.helpers.service import BaseConfdService


class RecordingAnnouncementService(BaseConfdService):
    resource_confd = 'recordings/announcements'

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._confd.recordings_announcements.get()

    def update(self, resource):
        return self._confd.recordings_announcements.update(resource)

    def list(self, **_ignored):
        return self.get()
