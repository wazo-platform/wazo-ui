# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import DhcpService
from .view import DhcpView

dhcp = create_blueprint('dhcp', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        DhcpView.service = DhcpService(clients['wazo_confd'])
        DhcpView.register(dhcp, route_base='/dhcp')
        register_flaskview(dhcp, DhcpView)

        core.register_blueprint(dhcp)
