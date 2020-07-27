# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import EndpointSIPTemplateService
from .view import EndpointSIPTemplateView

sip_template = create_blueprint('sip_template', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        EndpointSIPTemplateView.service = EndpointSIPTemplateService(clients['wazo_confd'])
        EndpointSIPTemplateView.register(sip_template, route_base='/sip_templates')
        register_flaskview(sip_template, EndpointSIPTemplateView)

        core.register_blueprint(sip_template)
