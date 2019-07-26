# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import SkillRuleForm


class SkillRuleView(BaseIPBXHelperView):
    form = SkillRuleForm
    resource = 'skillrule'

    @menu_item('.ipbx.callcenter.skillrules', l_('Skill Rules'), icon="sticky-note-o", multi_tenant=True)
    def index(self):
        return super().index()


class SkillRuleListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        skillrules = self.service.list(**params)
        results = [{'id': skillrule['id'], 'text': skillrule['name']} for skillrule in skillrules['items']]
        return jsonify(build_select2_response(results, skillrules['total'], params))
