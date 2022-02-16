# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import ContextService
from .view import ContextView, ContextListingView

context = create_blueprint('context', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ContextView.service = ContextService(clients['wazo_confd'])
        ContextView.register(context, route_base='/contexts')
        register_flaskview(context, ContextView)

        ContextListingView.service = ContextService(clients['wazo_confd'])
        ContextListingView.register(context, route_base='/contexts_listing')

        register_listing_url('context_by_type', 'context.ContextListingView:list_json_by_type')
        register_listing_url('context', 'context.ContextListingView:list_json')
        register_listing_url('context_with_id', 'context.ContextListingView:list_json_with_id')

        core.register_blueprint(context)
