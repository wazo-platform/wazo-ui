# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_ui.helpers.destination import register_destination_form
from wazo_ui.helpers.funckey import register_funckey_destination_form
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .form import ConferenceDestinationForm, ConferenceFuncKeyDestinationForm
from .service import ConferenceService
from .view import ConferenceDestinationView, ConferenceView

conference = create_blueprint('conference', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ConferenceView.service = ConferenceService(clients['wazo_confd'])
        ConferenceView.register(conference, route_base='/conferences')
        register_flaskview(conference, ConferenceView)

        ConferenceDestinationView.service = ConferenceService(clients['wazo_confd'])
        ConferenceDestinationView.register(
            conference, route_base='/conference_destination'
        )

        register_destination_form(
            'conference', l_('Conference'), ConferenceDestinationForm
        )
        register_funckey_destination_form(
            'conference', l_('Conference'), ConferenceFuncKeyDestinationForm
        )
        register_listing_url(
            'conference', 'conference.ConferenceDestinationView:list_json'
        )

        core.register_blueprint(conference)
