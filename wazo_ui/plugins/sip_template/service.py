# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class EndpointSIPTemplateService(BaseConfdService):

    resource_confd = 'endpoints_sip_templates'

    def __init__(self, confd_client):
        self._confd = confd_client
