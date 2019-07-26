# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class HepService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._convert_enabled(self._confd.hep_general.get())

    def update(self, resource):
        options = {'options': { k: v for k, v in resource.items() if v is not None }}
        return self._confd.hep_general.update(self._convert_enabled(options, True))

    def _convert_enabled(self, options, is_put=None):
        if options['options'].get('enabled') == True or options['options'].get('enabled') == '1':
            options['options']['enabled'] = '1' if is_put else 1
        else:
            options['options']['enabled'] = '0' if is_put else 0

        return options
