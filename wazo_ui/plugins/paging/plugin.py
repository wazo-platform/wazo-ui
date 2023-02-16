# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import PagingService
from .view import PagingView

paging = create_blueprint('paging', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PagingView.service = PagingService(clients['wazo_confd'])
        PagingView.register(paging, route_base='/pagings')
        register_flaskview(paging, PagingView)

        core.register_blueprint(paging)
