# Copyright 2017-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import MohService
from .view import MohListingView, MohView

moh = create_blueprint('moh', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        MohView.service = MohService(clients['wazo_confd'])
        MohView.register(moh, route_base='/moh')
        register_flaskview(moh, MohView)

        MohListingView.service = MohService(clients['wazo_confd'])
        MohListingView.register(moh, route_base='/moh_listing')

        register_listing_url('moh', 'moh.MohListingView:list_json')

        core.register_blueprint(moh)
