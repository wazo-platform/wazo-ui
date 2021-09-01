# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
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

from .form import SwitchboardForm


class SwitchboardView(BaseIPBXHelperView):
    form = SwitchboardForm
    resource = 'switchboard'

    @menu_item('.ipbx.services.switchboards', l_('Switchboards'), icon="desktop", multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        users = [user['uuid'] for user in resource['members']['users']]
        resource['members']['user_uuids'] = users
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(form.members.users)
        form.queue_music_on_hold.choices = self._build_set_choices_moh(form.queue_music_on_hold)
        form.waiting_room_music_on_hold.choices = self._build_set_choices_moh(form.waiting_room_music_on_hold)
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = '{} {}'.format(user.firstname.data, user.lastname.data)
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _build_set_choices_moh(self, moh):
        if not moh.data or moh.data == 'None':
            return []
        return [(moh.data, moh.data)]

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['members']['users'] = [{'uuid': user_uuid} for user_uuid in form.members.user_uuids.data]
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('switchboard', {}))
        return form


class SwitchboardDestinationView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        switchboards = self.service.list(**params)
        results = [{'id': sw['uuid'], 'text': sw['name']} for sw in switchboards['items']]
        return jsonify(build_select2_response(results, switchboards['total'], params))
