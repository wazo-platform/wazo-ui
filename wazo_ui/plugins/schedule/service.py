# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class ScheduleService(BaseConfdService):

    resource_confd = 'schedules'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def list_sound(self):
        return self._confd.sounds.list()

    def find_sound_by_path(self, sound_path):
        sounds = self.list_sound()['items']
        for sound in sounds:
            for file_ in sound['files']:
                for format_ in file_['formats']:
                    if sound['name'] == 'system':
                        if file_['name'] == sound_path:
                            return file_, format_
                    else:
                        if format_['path'] == sound_path:
                            return file_, format_
        return None, None
