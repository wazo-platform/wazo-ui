# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import AgentService
from .view import AgentView, AgentListingView

agent = create_blueprint('agent', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        AgentView.service = AgentService(clients['wazo_confd'])
        AgentView.register(agent, route_base='/agents')
        register_flaskview(agent, AgentView)

        AgentListingView.service = AgentService(clients['wazo_confd'])
        AgentListingView.register(agent, route_base='/agent_listing')

        register_listing_url('agent', 'agent.AgentListingView:list_json')

        core.register_blueprint(agent)
