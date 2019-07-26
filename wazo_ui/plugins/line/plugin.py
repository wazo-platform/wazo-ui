# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import LineService
from .view import LineView, LineListingView


line = create_blueprint('line', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        LineView.service = LineService(clients['wazo_confd'])
        LineView.register(line, route_base='/lines')
        register_flaskview(line, LineView)

        LineListingView.service = LineService(clients['wazo_confd'])
        LineListingView.register(line, route_base='/lines_listing')

        register_listing_url('line', 'line.LineListingView:list_json')

        core.register_blueprint(line)
