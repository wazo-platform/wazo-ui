# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import TransportService
from .view import TransportView

transport = create_blueprint('transports', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        TransportView.service = TransportService(clients['wazo_confd'])
        TransportView.register(transport, route_base='/transports')
        register_flaskview(transport, TransportView)

        core.register_blueprint(transport)
