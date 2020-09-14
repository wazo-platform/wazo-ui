# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging


logger = logging.getLogger(__name__)


class GlobalSettingsService(object):

    def __init__(self):
        pass

    def list(self):
        results = []
        return {'items': results}
