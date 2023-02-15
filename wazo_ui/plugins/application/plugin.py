# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url
from wazo_ui.core.form import register_destination_form_application

from .service import ApplicationService
from .view import ApplicationView, ApplicationDestinationView
from .form import (
    ApplicationCustomDestination,
    NodeDestinationForm,
    NoneDestinationForm,
    register_application_destination_form,
)

application = create_blueprint('application', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ApplicationView.service = ApplicationService(clients['wazo_confd'])
        ApplicationView.register(application, route_base='/applications')
        register_flaskview(application, ApplicationView)

        ApplicationDestinationView.service = ApplicationService(clients['wazo_confd'])
        ApplicationDestinationView.register(
            application, route_base='/applications_listing'
        )
        register_destination_form_application(
            'custom', l_('Custom'), ApplicationCustomDestination
        )

        register_application_destination_form(
            'None', l_('None'), NoneDestinationForm, position=0
        )
        register_application_destination_form('node', l_('Node'), NodeDestinationForm)

        # TODO: should register to something like application:custom, not only custom
        # But that would add another layer of logic in the template ...
        register_listing_url(
            'custom', 'application.ApplicationDestinationView:list_json'
        )

        core.register_blueprint(application)
