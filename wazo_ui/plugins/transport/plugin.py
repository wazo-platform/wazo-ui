# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import TransportService
from .view import TransportView, TransportDestinationView

transport = create_blueprint('transports', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        TransportView.service = TransportService(clients['wazo_confd'])
        TransportView.register(transport, route_base='/transports')
        register_flaskview(transport, TransportView)

        TransportDestinationView.service = TransportService(clients['wazo_confd'])
        TransportDestinationView.register(transport, route_base='/transports_listing')

        register_listing_url(
            'transport', 'transports.TransportDestinationView:list_json'
        )

        core.register_blueprint(transport)
