# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.extension import BaseConfdExtensionService


class ConferenceService(BaseConfdExtensionService):

    resource_confd = 'conferences'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_first_internal_context(self):
        result = self._confd.contexts.list(type='internal', limit=1, direction='asc', order='id')
        for context in result['items']:
            return context

    def get_context(self, context):
        result = self._confd.contexts.list(name=context)
        for context in result['items']:
            return context
