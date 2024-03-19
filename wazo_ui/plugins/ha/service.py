# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class HaService(BaseConfdService):
    resource_confd = 'ha'

    def __init__(self, confd):
        self._confd = confd

    def get(self):
        return self._confd.ha.get()

    def update(self, resource):
        return self._confd.ha.update(resource)
