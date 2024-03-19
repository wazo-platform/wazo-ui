# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class MohService(BaseConfdService):
    resource_confd = 'moh'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def download_filename(self, uuid, moh_filename):
        return self._confd.moh.download_file(uuid, moh_filename)

    def delete_filename(self, uuid, moh_filename):
        return self._confd.moh.delete_file(uuid, moh_filename)

    def upload_filename(self, uuid, moh_filename, binary_content):
        return self._confd.moh.upload_file(uuid, moh_filename, binary_content)
