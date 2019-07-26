# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import TrunkService
from .view import TrunkView, TrunkListingView


trunk = create_blueprint('trunk', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        TrunkView.service = TrunkService(clients['wazo_confd'])
        TrunkView.register(trunk, route_base='/trunks')
        register_flaskview(trunk, TrunkView)

        TrunkListingView.service = TrunkService(clients['wazo_confd'])
        TrunkListingView.register(trunk, route_base='/trunks_listing')

        register_listing_url('trunk', 'trunk.TrunkListingView:list_json')

        core.register_blueprint(trunk)
