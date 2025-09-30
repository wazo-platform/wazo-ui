# Copyright 2019-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint

from .service import HaService
from .view import HaView

ha = create_blueprint('ha', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        HaView.service = HaService(clients['wazo_confd'])
        HaView.register(ha, route_base='/ha')
        register_flaskview(ha, HaView)

        core.register_blueprint(ha)
