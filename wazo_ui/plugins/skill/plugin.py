# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import SkillService
from .view import SkillView, SkillListingView

skill = create_blueprint('skill', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        SkillView.service = SkillService(clients['wazo_confd'])
        SkillView.register(skill, route_base='/skills')
        register_flaskview(skill, SkillView)

        SkillListingView.service = SkillService(clients['wazo_confd'])
        SkillListingView.register(skill, route_base='/skill_listing')

        register_listing_url('skill', 'skill.SkillListingView:list_json')

        core.register_blueprint(skill)
