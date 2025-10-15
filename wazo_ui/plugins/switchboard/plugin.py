# Copyright 2017-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.destination import register_destination_form
from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .form import SwitchboardDestinationForm
from .service import SwitchboardService
from .view import SwitchboardDestinationView, SwitchboardView

switchboard = create_blueprint('switchboard', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        SwitchboardView.service = SwitchboardService(clients['wazo_confd'])
        SwitchboardView.register(switchboard, route_base='/switchboards')
        register_flaskview(switchboard, SwitchboardView)

        SwitchboardDestinationView.service = SwitchboardService(clients['wazo_confd'])
        SwitchboardDestinationView.register(
            switchboard, route_base='/switchboard_destination'
        )

        register_destination_form(
            'switchboard', l_('Switchboard'), SwitchboardDestinationForm
        )
        register_listing_url(
            'switchboard', 'switchboard.SwitchboardDestinationView:list_json'
        )

        core.register_blueprint(switchboard)
