# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService


class AccessFeaturesService(BaseConfdService):

    resource_confd = 'access_features'

    def __init__(self, confd_client):
        self._confd = confd_client
