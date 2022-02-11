# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import VoicemailForm


class VoicemailView(BaseIPBXHelperView):
    form = VoicemailForm
    resource = 'voicemail'

    @menu_item('.ipbx.user_management.voicemails', l_('Voicemails'), order=5, icon="envelope", multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        users = [user['uuid'] for user in resource['users']]
        resource['user_uuid'] = users
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.user_uuid.choices = self._build_set_choices_users(form.users)
        form.context.choices = self._build_set_choices_context(form.context)
        return form

    def _build_set_choices_context(self, context):
        if not context.data or context.data == 'None':
            return []
        return [(context.data, context.data)]

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = '{} {}'.format(user.firstname.data, user.lastname.data)
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        if form.user_uuid.data and form.user_uuid.data != 'None':
            resource['users'] = [{'uuid': form.user_uuid.data}]
        else:
            resource['users'] = []
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('voicemail', {}))
        return form


class VoicemailDestinationView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        voicemails = self.service.list(**params)
        results = [{'id': vm['id'], 'text': vm['name']} for vm in voicemails['items']]
        return jsonify(build_select2_response(results, voicemails['total'], params))
