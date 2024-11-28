# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class PhoneNumberService(BaseConfdService):
    resource_confd = 'phone_numbers'

    def __init__(self, confd_client):
        self._confd = confd_client
