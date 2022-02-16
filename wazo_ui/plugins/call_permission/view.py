# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView, NewHelperViewMixin

from .form import CallPermissionForm, mode_map


class CallPermissionView(NewHelperViewMixin, BaseIPBXHelperView):
    form = CallPermissionForm
    resource = 'call_permission'

    @menu_item('.ipbx.call_management.callpermissions', l_('Call Permissions'), icon='ban', multi_tenant=True)
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=resource_list,
                               listing_urls=self.listing_urls,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               mode_map=mode_map)

    def _map_resources_to_form(self, resource):
        resource['user_uuids'] = [user['uuid'] for user in resource['users']]
        resource['group_ids'] = [group['id'] for group in resource['groups']]
        resource['outcall_ids'] = [outcall['id'] for outcall in resource['outcalls']]
        resource['extensions'] = [{'exten': exten} for exten in resource['extensions']]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.user_uuids.choices = self._build_set_choices_users(form.users)
        form.group_ids.choices = self._build_set_choices_groups(form.groups)
        form.outcall_ids.choices = self._build_set_choices_outcalls(form.outcalls)
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

    def _build_set_choices_outcalls(self, outcalls):
        return [(outcall.form.id.data, outcall.form.name.data) for outcall in outcalls]

    def _map_form_to_resources(self, form, form_id=None):
        data = super()._map_form_to_resources(form, form_id)
        data['user_uuids'] = [user_uuid for user_uuid in form.user_uuids.data]
        data['group_ids'] = [group_id for group_id in form.group_ids.data]
        data['outcall_ids'] = [outcall_id for outcall_id in form.outcall_ids.data]
        data['extensions'] = [extension['exten'] for extension in data['extensions']]
        return data


class CallPermissionListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        callpermissions = self.service.list(**params)
        results = [{'id': callpermission['id'], 'text': callpermission['name']}
                   for callpermission in callpermissions['items']]
        return jsonify(build_select2_response(results, callpermissions['total'], params))
