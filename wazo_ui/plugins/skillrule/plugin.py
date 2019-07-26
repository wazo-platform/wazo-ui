# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import SkillRuleService
from .view import SkillRuleView, SkillRuleListingView

skillrule = create_blueprint('skillrule', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        SkillRuleView.service = SkillRuleService(clients['wazo_confd'])
        SkillRuleView.register(skillrule, route_base='/skillrules')
        register_flaskview(skillrule, SkillRuleView)

        SkillRuleListingView.service = SkillRuleService(clients['wazo_confd'])
        SkillRuleListingView.register(skillrule, route_base='/skillrule_listing')

        register_listing_url('skillrule', 'skillrule.SkillRuleListingView:list_json')

        core.register_blueprint(skillrule)
