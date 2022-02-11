# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class ApplicationService(BaseConfdService):

    resource_confd = 'applications'

    def __init__(self, confd_client):
        self._confd = confd_client

    def create(self, resource):
        application_created = super().create(resource)
        resource['uuid'] = application_created['uuid']
