# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.destination import register_destination_form
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .form import IvrDestinationForm
from .service import IvrService
from .view import IvrDestinationView, IvrView

ivr = create_blueprint('ivr', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        IvrView.service = IvrService(clients['wazo_confd'])
        IvrView.register(ivr, route_base='/ivrs')
        register_flaskview(ivr, IvrView)

        IvrDestinationView.service = IvrService(clients['wazo_confd'])
        IvrDestinationView.register(ivr, route_base='/ivr_destination')

        register_destination_form('ivr', 'Ivr', IvrDestinationForm)
        register_listing_url('ivr', 'ivr.IvrDestinationView:list_json')

        core.register_blueprint(ivr)
