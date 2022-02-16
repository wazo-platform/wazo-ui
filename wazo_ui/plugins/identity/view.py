# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import (
    jsonify,
    flash,
    request,
    render_template,
    redirect,
    url_for,
)
from flask_babel import lazy_gettext as l_
from flask_classful import route

from requests.exceptions import HTTPError

from wazo_ui.helpers.tenant import refresh_tenants
from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import (
    GroupForm,
    IdentityForm,
    LDAPForm,
    PolicyForm,
    TenantForm,
)


class IdentityView(BaseIPBXHelperView):
    form = IdentityForm
    resource = 'identity'

    @menu_item('.ipbx.identity', l_('Credentials'), icon="user-secret", multi_tenant=True)
    @menu_item('.ipbx.identity.identities', l_('Identities'), order=1, icon="user", multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['members']['group_uuids'] = [group['uuid'] for group in resource['members']['groups']]
        resource['members']['policy_uuids'] = [policy['uuid'] for policy in resource['members']['policies']]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.group_uuids.choices = self._build_set_choices_groups(form.members.groups)
        form.members.policy_uuids.choices = self._build_set_choices_policies(form.members.policies)
        return form

    def _build_set_choices_groups(self, groups):
        results = []
        for group in groups:
            results.append((group.form.uuid.data, group.form.name.data))
        return results

    def _build_set_choices_policies(self, policies):
        results = []
        for policy in policies:
            results.append((policy.form.uuid.data, policy.form.name.data))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = form.to_dict()
        if form_id:
            resource['uuid'] = form_id
        resource['members']['groups'] = [{'uuid': group_uuid} for group_uuid in form.members.group_uuids.data]
        resource['members']['policies'] = [{'uuid': policy_uuid} for policy_uuid in form.members.policy_uuids.data]
        return resource


class IdentityListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        identities = self.service.list(**params)
        results = [{'id': identity['uuid'], 'text': identity['username']} for identity in identities['items']]
        return jsonify(build_select2_response(results, identities['total'], params))


class GroupView(BaseIPBXHelperView):
    form = GroupForm
    resource = 'identity_group'

    @menu_item('.ipbx.identity.groups', l_('Groups'), order=2, icon="users", multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['members']['user_uuids'] = [user['uuid'] for user in resource['members']['users']]
        resource['members']['policy_uuids'] = [policy['uuid'] for policy in resource['members']['policies']]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(form.members.users)
        form.members.policy_uuids.choices = self._build_set_choices_policies(form.members.policies)
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            results.append((user.uuid.data, user.username.data))
        return results

    def _build_set_choices_policies(self, policies):
        results = []
        for policy in policies:
            results.append((policy.form.uuid.data, policy.form.name.data))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['members']['users'] = [{'uuid': user_uuid} for user_uuid in form.members.user_uuids.data]
        resource['members']['policies'] = [{'uuid': policy_uuid} for policy_uuid in form.members.policy_uuids.data]
        return resource


class GroupListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        groups = self.service.list(**params)
        results = [{'id': group['uuid'], 'text': group['name']} for group in groups['items']]
        return jsonify(build_select2_response(results, groups['total'], params))


class TenantView(BaseIPBXHelperView):
    form = TenantForm
    resource = 'tenant'

    @menu_item('.ipbx.global_settings.tenants', l_('Tenants'), order=3, icon="building")
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
                               current_breadcrumbs=self._get_current_breadcrumbs())

    def post(self):
        result = super().post()
        refresh_tenants()

        return result

    @route('/put/<id>', methods=['POST'])
    def put(self, id):
        result = super().put(id)
        refresh_tenants()

        return result

    @route('/delete/<id>', methods=['GET'])
    def delete(self, id):
        result = super().delete(id)
        refresh_tenants()

        return result

    def _map_resources_to_form(self, resource):
        resource['members']['user_uuids'] = [user['uuid'] for user in resource['members']['users']]
        resource['members']['policy_uuids'] = [policy['uuid'] for policy in resource['members']['policies']]
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(form.members.users)
        form.members.policy_uuids.choices = self._build_set_choices_policies(form.members.policies)
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            results.append((user.uuid.data, user.username.data))
        return results

    def _build_set_choices_policies(self, policies):
        results = []
        for policy in policies:
            results.append((policy.form.uuid.data, policy.form.name.data))
        return results


class TenantListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        tenants = self.service.list(**params)
        results = [{'id': tenant['uuid'], 'text': tenant['name']} for tenant in tenants['items']]
        return jsonify(build_select2_response(results, tenants['total'], params))


class PolicyView(BaseIPBXHelperView):
    form = PolicyForm
    resource = 'policy'

    @menu_item('.ipbx.identity.policies', l_('Policies'), order=4, icon="lock", multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        resource['acl'] = [{'value': access} for access in resource['acl']]
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['acl'] = [access['value'] for access in resource['acl']]
        return resource


class PolicyListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        groups = self.service.list(**params)
        results = [{'id': group['uuid'], 'text': group['name']} for group in groups['items']]
        return jsonify(build_select2_response(results, groups['total'], params))


class LDAPConfigView(BaseIPBXHelperView):
    form = LDAPForm
    resource = 'ldap'

    @menu_item('.ipbx.identity.ldap', l_('LDAP'), order=5, icon="wrench", multi_tenant=True)
    def index(self, form=None):
        resource = self.service.get()
        form = form or self.form()
        return render_template(self._get_template('index'),
                               form=self.form(data=resource))

    def _map_form_to_resources_post(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['protocol_security'] = self._convert_empty_string_to_none(form.protocol_security.data)
        return resource

    def post(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self.index(form)

        resource = self._map_form_to_resources_post(form)
        try:
            self.service.update(resource)
        except HTTPError as error:
            self._flash_http_error(error)
            return self.index()

        flash(l_('LDAP config has been updated'), 'success')
        return self._redirect_for('index')

    @route('/delete', methods=['GET'])
    def delete(self):
        try:
            self.service.delete()
            flash(l_('%(resource)s: LDAP configuration has been deleted', resource=self.resource), 'success')
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_referrer_or('index')
