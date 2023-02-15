# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import request, jsonify
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import AgentForm


class AgentView(BaseIPBXHelperView):
    form = AgentForm
    resource = 'agent'
    raw_skills = []

    @menu_item('.ipbx.callcenter.agents', l_('Agents'), icon="users", multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        # Trick to store ids and names directly and map them in _populate_form,
        # because wtforms will map name to `skill-0` ...
        self.raw_skills = resource['skills']

        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        for idx, raw_skill in enumerate(self.raw_skills):
            form.skills[idx].skill_id.choices = [(raw_skill['id'], raw_skill['name'])]

        return form


class AgentListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        agents = self.service.list(**params)
        results = [
            {'id': agent['id'], 'text': agent['number']} for agent in agents['items']
        ]
        return jsonify(build_select2_response(results, agents['total'], params))
