# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

logger = logging.getLogger(__name__)


class CdrService:
    def __init__(self, call_logd_client):
        self._call_logd = call_logd_client

    def list(
        self, limit=None, order=None, direction=None, offset=None, search=None, **kwargs
    ):
        return self._call_logd.cdr.list(
            search=search,
            order=order,
            limit=limit,
            direction=direction,
            offset=offset,
            **kwargs
        )
