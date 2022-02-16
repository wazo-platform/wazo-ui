# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import EndpointSIPTemplateService
from .view import EndpointSIPTemplateView, SIPTemplateDestinationView

sip_template = create_blueprint('sip_template', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        EndpointSIPTemplateView.service = EndpointSIPTemplateService(clients['wazo_confd'])
        EndpointSIPTemplateView.register(sip_template, route_base='/sip_templates')
        register_flaskview(sip_template, EndpointSIPTemplateView)

        SIPTemplateDestinationView.service = EndpointSIPTemplateService(clients['wazo_confd'])
        SIPTemplateDestinationView.register(sip_template, route_base='/sip_templates_listing')

        register_listing_url('sip_template', 'sip_template.SIPTemplateDestinationView:list_json')

        core.register_blueprint(sip_template)
