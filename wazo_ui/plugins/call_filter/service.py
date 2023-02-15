# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class CallFilterService(BaseConfdService):
    resource_confd = 'call_filters'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def create(self, resource):
        callfilter_id = super().create(resource)['id']
        self._confd.call_filters(callfilter_id).update_user_recipients(
            resource['recipients_user']
        )
        self._confd.call_filters(callfilter_id).update_user_surrogates(
            resource['surrogates_user']
        )

    def update(self, resource):
        super().update(resource)
        self._confd.call_filters(resource['id']).update_user_recipients(
            resource['recipients_user']
        )
        self._confd.call_filters(resource['id']).update_user_surrogates(
            resource['surrogates_user']
        )
        self._confd.call_filters(resource['id']).update_fallbacks(resource['fallbacks'])

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

    def get_bsfilter_extension(self):
        extensions = self._confd.extensions_features.list(feature='bsfilter')['items']
        for extension in extensions:
            return extension
        return None

    def list_user(self, **kwargs):
        return self._confd.users.list(**kwargs)

    def get_user_by_uuid(self, uuid):
        return self._confd.users.get(uuid)
