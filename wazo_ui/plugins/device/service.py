# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class DeviceService(BaseConfdService):

    resource_confd = 'devices'

    def __init__(self, confd_client, provd_client):
        self._confd = confd_client
        self._provd = provd_client

    def list_unallocated(self, limit=None, order=None, direction=None, offset=None, search=None, **kwargs):
        return self._confd.unallocated_devices.list(search=search,
                                                    order=order,
                                                    limit=limit,
                                                    direction=direction,
                                                    offset=offset,
                                                    **kwargs)

    def autoprov(self, device_id):
        self._confd.devices.autoprov(device_id)
        self.synchronize(device_id)

    def synchronize(self, device_id):
        self._confd.devices.synchronize(device_id)

    def assign_tenant(self, device_id):
        self._confd.unallocated_devices.assign_tenant(device_id)

    def get_config(self, config_id):
        return self._provd.configs.get(config_id)

    def delete(self, device_id):
        self.autoprov(device_id)
        super().delete(device_id)
