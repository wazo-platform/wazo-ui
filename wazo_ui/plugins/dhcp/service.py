# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class DhcpService(BaseConfdService):
    resource_confd = 'dhcp'

    def __init__(self, confd):
        self._confd = confd

    def get(self):
        return self._confd.dhcp.get()

    def update(self, resource):
        return self._confd.dhcp.update(resource)
