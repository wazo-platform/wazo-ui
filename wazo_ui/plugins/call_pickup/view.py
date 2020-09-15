# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import CallPickupForm


class CallPickupView(BaseIPBXHelperView):
    form = CallPickupForm
    resource = 'call_pickup'

    @menu_item('.ipbx.call_management.callpickups', l_('Call Pickups'), icon='rotate-left', multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['interceptors']['user_uuids'] = [user['uuid'] for user in resource['interceptors']['users']]
        resource['targets']['user_uuids'] = [user['uuid'] for user in resource['targets']['users']]
        resource['interceptors']['group_ids'] = [group['id'] for group in resource['interceptors']['groups']]
        resource['targets']['group_ids'] = [group['id'] for group in resource['targets']['groups']]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.interceptors.form.user_uuids.choices = self._build_set_choices_users(form.interceptors.form.users)
        form.interceptors.form.group_ids.choices = self._build_set_choices_groups(form.interceptors.form.groups)
        form.targets.form.user_uuids.choices = self._build_set_choices_users(form.targets.form.users)
        form.targets.form.group_ids.choices = self._build_set_choices_groups(form.targets.form.groups)
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.form.lastname.data:
                text = '{} {}'.format(user.form.firstname.data, user.form.lastname.data)
            else:
                text = user.form.firstname.data
            results.append((user.form.uuid.data, text))
        return results

    def _build_set_choices_groups(self, groups):
        return [(group.form.id.data, group.form.name.data) for group in groups]

    def _map_form_to_resources(self, form, form_id=None):
        data = super()._map_form_to_resources(form, form_id)
        data['interceptors']['users'] = [{'uuid': user_uuid} for user_uuid in data['interceptors']['user_uuids']]
        data['targets']['users'] = [{'uuid': user_uuid} for user_uuid in data['targets']['user_uuids']]
        data['interceptors']['groups'] = [{'id': group_id} for group_id in data['interceptors']['group_ids']]
        data['targets']['groups'] = [{'id': group_id} for group_id in data['targets']['group_ids']]
        return data
