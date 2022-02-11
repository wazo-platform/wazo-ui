# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class VoicemailService(BaseConfdService):

    resource_confd = 'voicemails'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def create(self, voicemail):
        users = voicemail['users']
        voicemail = self._confd.voicemails.create(voicemail)
        for user in users:
            self._confd.voicemails(voicemail).add_user(user['uuid'])

    def update(self, voicemail):
        self._confd.voicemails(voicemail).remove_users()
        for user in voicemail['users']:
            self._confd.voicemails(voicemail).add_user(user['uuid'])

        self._confd.voicemails.update(voicemail)

    def delete(self, id):
        voicemail = self._confd.voicemails.get(id)
        for user in voicemail['users']:
            self._confd.voicemails(voicemail).remove_user(user['uuid'])

        self._confd.voicemails.delete(voicemail)
