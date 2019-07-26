# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class CallPickupService(BaseConfdService):
    resource_confd = 'call_pickups'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def create(self, resource):
        resource_created = super().create(resource)
        self._confd.call_pickups(resource_created['id']).update_user_interceptors(resource['interceptors']['users'])
        self._confd.call_pickups(resource_created['id']).update_user_targets(resource['targets']['users'])
        self._confd.call_pickups(resource_created['id']).update_group_interceptors(resource['interceptors']['groups'])
        self._confd.call_pickups(resource_created['id']).update_group_targets(resource['targets']['groups'])
        return resource_created

    def update(self, resource):
        super().update(resource)
        self._confd.call_pickups(resource['id']).update_user_interceptors(resource['interceptors']['users'])
        self._confd.call_pickups(resource['id']).update_user_targets(resource['targets']['users'])
        self._confd.call_pickups(resource['id']).update_group_interceptors(resource['interceptors']['groups'])
        self._confd.call_pickups(resource['id']).update_group_targets(resource['targets']['groups'])
