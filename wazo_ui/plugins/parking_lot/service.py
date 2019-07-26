# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.extension import BaseConfdExtensionService


class ParkingLotService(BaseConfdExtensionService):

    resource_confd = 'parking_lots'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
