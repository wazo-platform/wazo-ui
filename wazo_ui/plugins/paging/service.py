# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class PagingService(BaseConfdService):
    resource_confd = 'pagings'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def create(self, resource):
        paging_created = super().create(resource)
        resource['id'] = paging_created['id']
        self._update_members_callers(resource)

    def update(self, resource):
        super().update(resource)
        self._update_members_callers(resource)

    def _update_members_callers(self, paging):
        members = paging.get('members')
        callers = paging.get('callers')

        if members:
            self._confd.pagings(paging).update_user_members(members.get('users'))
        if callers:
            self._confd.pagings(paging).update_user_callers(callers.get('users'))
