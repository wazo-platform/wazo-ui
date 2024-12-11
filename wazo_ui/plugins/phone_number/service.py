# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class PhoneNumberService(BaseConfdService):
    resource_confd = 'phone_numbers'

    def __init__(self, confd_client):
        self._confd = confd_client

    def select_main_number(self, number_uuid):
        resource_client = getattr(self._confd, self.resource_confd)
        body = {'phone_number_uuid': number_uuid}
        resource_client.set_main(body)
