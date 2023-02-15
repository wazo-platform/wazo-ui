# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import OutcallService
from .view import OutcallView, OutcallDestinationView

outcall = create_blueprint('outcall', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        OutcallView.service = OutcallService(clients['wazo_confd'])
        OutcallView.register(outcall, route_base='/outcalls')
        register_flaskview(outcall, OutcallView)

        OutcallDestinationView.service = OutcallService(clients['wazo_confd'])
        OutcallDestinationView.register(outcall, route_base='/outcall_destination')

        register_listing_url('outcall', 'outcall.OutcallDestinationView:list_json')

        core.register_blueprint(outcall)
