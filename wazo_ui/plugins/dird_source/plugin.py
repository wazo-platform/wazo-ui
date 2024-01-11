# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import DirdSourceService
from .view import DirdSourceListingView, DirdSourceView

dird_source = create_blueprint('dird_source', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        DirdSourceView.service = DirdSourceService(clients['wazo_dird'])
        DirdSourceView.register(dird_source, route_base='/dird_sources')
        register_flaskview(dird_source, DirdSourceView)

        DirdSourceListingView.service = DirdSourceService(clients['wazo_dird'])
        DirdSourceListingView.register(dird_source, route_base='/dird_sources_listing')

        register_listing_url(
            'dird_source', 'dird_source.DirdSourceListingView:list_json'
        )

        core.register_blueprint(dird_source)
