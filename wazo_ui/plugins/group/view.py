# Copyright 2017-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import GroupForm


class GroupView(BaseIPBXHelperView):
    form = GroupForm
    resource = 'group'

    @menu_item(
        '.ipbx.user_management.groups',
        l_('Ring Groups'),
        order=2,
        icon="users",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['members']['user_uuids'] = [
            user['uuid'] for user in resource['members']['users']
        ]
        resource['extensions_members'] = resource['members']['extensions']
        resource['call_permission_ids'] = [
            call_permission['id'] for call_permission in resource['call_permissions']
        ]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(
            form.members.users
        )
        form.extensions[0].exten.choices = self._build_set_choices_exten(
            form.extensions[0]
        )
        form.extensions[0].context.choices = self._build_set_choices_context(
            form.extensions[0]
        )
        form.music_on_hold.choices = self._build_set_choices_moh(form.music_on_hold)
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(
            form.schedules[0]
        )
        form.call_permission_ids.choices = self._build_set_choices_callpermissions(
            form.call_permissions
        )
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = f'{user.firstname.data} {user.lastname.data}'
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _build_set_choices_exten(self, extension):
        if not extension.exten.data or extension.exten.data == 'None':
            return []
        return [(extension.exten.data, extension.exten.data)]

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            context = self.service.get_first_internal_context()
        else:
            context = self.service.get_context(extension.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(extension.context.data, extension.context.data)]

    def _build_set_choices_moh(self, moh):
        if not moh.data or moh.data == 'None':
            return []
        moh_object = self.service.get_music_on_hold(moh.data)
        if moh_object is None:
            return []
        moh_label = moh_object['label']
        return [(moh.data, f"{moh_label} ({moh.data})")]

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

    def _build_set_choices_callpermissions(self, call_permissions):
        return [
            (call_permission.form.id.data, call_permission.form.name.data)
            for call_permission in call_permissions
        ]

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['members']['users'] = [
            {'uuid': user_uuid} for user_uuid in form.members.user_uuids.data
        ]
        resource['call_permissions'] = [
            {'id': call_permission_id}
            for call_permission_id in form.call_permission_ids.data
        ]
        resource['music_on_hold'] = form.music_on_hold.data
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('group', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form


class GroupDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        groups = self.service.list(**params)
        results = [
            {'id': group['id'], 'text': group['label']} for group in groups['items']
        ]
        return jsonify(build_select2_response(results, groups['total'], params))
