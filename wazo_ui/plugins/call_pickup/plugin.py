# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import CallPickupService
from .view import CallPickupView

call_pickup = create_blueprint('call_pickup', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        CallPickupView.service = CallPickupService(clients['wazo_confd'])
        CallPickupView.register(call_pickup, route_base='/callpickups')
        register_flaskview(call_pickup, CallPickupView)

        core.register_blueprint(call_pickup)
