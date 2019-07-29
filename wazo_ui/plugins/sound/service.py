# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class SoundService(BaseConfdService):

    resource_confd = 'sounds'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self):
        return self._confd.sounds.list()

    def get(self, tenant_uuid, category):
        return self._confd.sounds.get(category, tenant_uuid=tenant_uuid)

    def delete(self, tenant_uuid, category):
        self._confd.sounds.delete(category, tenant_uuid=tenant_uuid)

    def download_sound_filename(self, tenant_uuid, category, file_name, **kwargs):
        return self._confd.sounds.download_file(category, file_name, tenant_uuid=tenant_uuid, **kwargs)

    def delete_sound_filename(self, tenant_uuid, category, sound_filename, **kwargs):
        self._confd.sounds.delete_file(category, sound_filename, tenant_uuid=tenant_uuid, **kwargs)

    def upload_sound_filename(self, tenant_uuid, category, sound_filename, binary_content, **kwargs):
        self._confd.sounds.upload_file(category, sound_filename, binary_content, tenant_uuid=tenant_uuid, **kwargs)
