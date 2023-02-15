# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import SkillForm


class SkillView(BaseIPBXHelperView):
    form = SkillForm
    resource = 'skill'

    @menu_item(
        '.ipbx.callcenter.skills', l_('Skills'), icon="trophy", multi_tenant=True
    )
    def index(self):
        return super().index()


class SkillListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        skills = self.service.list(**params)
        results = [
            {'id': skill['id'], 'text': skill['name']} for skill in skills['items']
        ]
        return jsonify(build_select2_response(results, skills['total'], params))
