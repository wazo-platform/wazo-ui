# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import request, jsonify, redirect, url_for, render_template, flash
from flask_classful import route
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView
from wazo_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params
)

from .form import DirdSourceForm


class DirdSourceView(BaseIPBXHelperView):
    form = DirdSourceForm
    resource = 'dird_source'

    @menu_item('.ipbx.dird.source', l_('Sources'), icon='random', multi_tenant=True)
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = {"items": []}
            for source in self.service.list()['items']:
                source['get_url'] = "{}/".format(source['backend'])
                resource_list['items'].append(source)
            backend_list = self.service.list_backends()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=resource_list,
                               backend_list=backend_list,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               listing_urls=self.listing_urls)

    @route('/new/<backend>', methods=['GET'])
    def new(self, backend):
        default_auth_config = {
            'host': 'localhost',
            'port': 9497,
            'timeout': '',
            'prefix_': None,
            'https': False,
            'verify_certificate': False,
            'certificate_path': '',
            'version': '0.1',
        }
        default_confd_config = {
            'host': 'localhost',
            'port': 9486,
            'timeout': '',
            'prefix_': None,
            'https': False,
            'verify_certificate': False,
            'certificate_path': '',
            'version': '1.1',
        }
        default = {
            'conference_config': {
                'auth': dict(
                    key_file='/var/lib/wazo-auth-keys/wazo-dird-conference-backend-key.yml',
                    **default_auth_config,
                ),
                'confd': default_confd_config,
                'format_columns': [
                    {'key': 'phone', 'value': '{extensions[0]}'},
                    {'key': 'reverse', 'value': '{name}'},
                ],
                'searched_columns': [
                    {'value': 'name'},
                    {'value': 'extensions'},
                    {'value': 'incalls'},
                ],
            },
            'ldap_config': {
                'format_columns': [
                    {'key': 'name', 'value': '{givenName} {sn}'},
                    {'key': 'phone', 'value': '{telephoneNumber}'},
                ],
                'searched_columns': [
                    {'value': 'givenName'},
                    {'value': 'sn'},
                ]
            },
            'csv_ws_office': {
                'timeout': 10,
            },
            'office365_config': {
                'auth': {
                    'port': 9497,
                    'timeout': 0,
                    'verify_certificate': True,
                    'version': '0.1',
                },
                'endpoint': 'https://graph.microsoft.com/v1.0/me/contacts',
            },
            'google_config': {
                'auth': default_auth_config,
                'searched_columns': [
                    {'value': 'name'},
                    {'value': 'numbers'},
                ],
                'first_matched_columns': [
                    {'value': 'numbers'},
                ],
                'format_columns': [
                    {'key': 'reverse', 'value': '{name}'},
                    {'key': 'phone', 'value': '{numbers[0]}'},
                    {'key': 'phone_mobile', 'value': '{numbers_by_label[mobile]}'},
                ],

            },
            'phonebook_config': {
                'searched_columns': [
                    {'value': 'firstname'},
                    {'value': 'lastname'},
                    {'value': 'email'},
                    {'value': 'phone'},
                    {'value': 'mobile_phone'},
                ],
                'first_matched_columns': [
                    {'value': 'phone'},
                    {'value': 'mobile_phone'},
                    {'value': 'fax'},
                ],
                'format_columns': [
                    {'key': 'name', 'value': '{firstname} {lastname}'},
                    {'key': 'reverse', 'value': '{firstname} {lastname}'},
                    {'key': 'phone_mobile', 'value': '{mobile_phone}'},
                ],
            },
            'wazo_config': {
                'auth': dict(
                    key_file='/var/lib/wazo-auth-keys/wazo-dird-wazo-backend-key.yml',
                    **default_auth_config
                ),
                'confd': default_confd_config,
                'searched_columns': [
                    {'value': 'firstname'},
                    {'value': 'lastname'},
                    {'value': 'exten'},
                ],
                'first_matched_columns': [
                    {'value': 'mobile_phone_number'},
                    {'value': 'exten'},
                ],
                'format_columns': [
                    {'key': 'name', 'value': '{firstname} {lastname}'},
                    {'key': 'phone', 'value': '{exten}'},
                    {'key': 'reverse', 'value': '{firstname} {lastname}'},
                ],
            }
        }
        form = self.form(backend=backend, data=default)

        return render_template(self._get_template(backend=backend),
                               form_mode='add',
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               form=form)

    @route('/get/<backend>/<id>')
    def get(self, backend, id):
        return self._get(backend, id)

    def _get(self, backend, id, form=None):
        try:
            resource = self.service.get(backend, id)
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        form = form or self._map_resources_to_form(resource)
        form = self._populate_form(form)

        return render_template(self._get_template(backend=backend),
                               form=form,
                               resource=resource,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               listing_urls=self.listing_urls)

    def post(self):
        form = self.form()
        resources = self._map_form_to_resources_post(form)

        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._new(form)

        try:
            self.service.create(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._new(form)

        flash('Resource has been created', 'success')
        return self._redirect_for('index')

    @route('/put/<backend>/<id>', methods=['POST'])
    def put(self, backend, id):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._get(backend, id, form)

        resources = self._map_form_to_resources_put(form, id)
        try:
            self.service.update(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._get(backend, id, form)

        flash(l_('%(resource)s: Resource has been updated', resource=self.resource), 'success')
        return self._redirect_referrer_or('index')

    @route('/delete/<backend>/<id>', methods=['GET'])
    def delete(self, backend, id):
        try:
            self.service.delete(backend, id)
            flash(l_('%(resource)s: Resource %(id)s has been deleted', resource=self.resource, id=id), 'success')
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_referrer_or('index')

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        backend = resource['backend']
        config_name = backend + '_config'

        if 'confd' in resource[config_name]:
            if not resource[config_name]['confd']['timeout']:
                del resource[config_name]['confd']['timeout']

        if 'auth' in resource[config_name] and backend != 'office365' and backend != 'google':
            if not resource[config_name]['auth']['timeout']:
                del resource[config_name]['auth']['timeout']

        if 'format_columns' in resource[config_name]:
            resource[config_name]['format_columns'] = {option['key']: option['value'] for option in
                                                       resource[config_name]['format_columns']}

        if 'searched_columns' in resource[config_name]:
            resource[config_name]['searched_columns'] = [option['value'] for option in
                                                         resource[config_name]['searched_columns']]

        if 'first_matched_columns' in resource[config_name]:
            resource[config_name]['first_matched_columns'] = [option['value'] for option in
                                                              resource[config_name]['first_matched_columns']]

        if 'delimiter' in resource[config_name]:
            resource[config_name]['separator'] = resource[config_name]['delimiter']

        if 'prefix_' in resource[config_name].get('auth', {}):
            resource[config_name]['auth']['prefix'] = resource[config_name]['auth'].pop('prefix_')

        if 'prefix_' in resource[config_name].get('confd', {}):
            resource[config_name]['confd']['prefix'] = resource[config_name]['confd'].pop('prefix_')

        # Handle `verify_certificate` for office 365 or google that can be True, False or the value of certificate_path
        if backend in ('office365', 'google', 'conference', 'wazo'):
            path = resource[config_name]['auth'].get('certificate_path')
            verify = resource[config_name]['auth']['verify_certificate']

            if verify and path:
                verify_certificate = path
            else:
                verify_certificate = verify

            resource[config_name]['auth']['verify_certificate'] = verify_certificate

        if backend in ('conference', 'wazo'):
            path = resource[config_name]['confd'].get('certificate_path')
            verify = resource[config_name]['confd']['verify_certificate']

            if verify and path:
                verify_certificate = path
            else:
                verify_certificate = verify

            resource[config_name]['confd']['verify_certificate'] = verify_certificate

        return resource

    def _map_resources_to_form(self, resource):
        backend = resource['backend']
        config_name = backend + '_config'

        # separator can't be used an a field for wtforms ...
        if 'separator' in resource:
            resource['delimiter'] = resource['separator']

        resource[config_name] = resource

        if 'format_columns' in resource[config_name]:
            resource[config_name]['format_columns'] = [{'key': key, 'value': val} for (key, val) in
                                                       resource[config_name]['format_columns'].items()]

        if 'searched_columns' in resource[config_name]:
            resource[config_name]['searched_columns'] = [{'value': option} for option in
                                                         resource[config_name]['searched_columns']]

        if 'first_matched_columns' in resource[config_name]:
            resource[config_name]['first_matched_columns'] = [{'value': option} for option in
                                                              resource[config_name]['first_matched_columns']]

        if 'prefix' in resource[config_name].get('auth', {}):
            resource[config_name]['auth']['prefix_'] = resource[config_name]['auth'].pop('prefix')

        if 'prefix' in resource[config_name].get('confd', {}):
            resource[config_name]['confd']['prefix_'] = resource[config_name]['confd'].pop('prefix')

        # Handle `verify_certificate` for office 365 or google that can be True, False or the value of certificate_path
        if backend in ('office365', 'google', 'conference', 'wazo'):
            verify_certificate = resource[config_name]['auth'].get('verify_certificate')
            if verify_certificate in (True, False):
                verify = verify_certificate
            else:
                verify = True
                resource[config_name]['auth']['certificate_path'] = verify_certificate

            resource[config_name]['auth']['verify_certificate'] = verify

        if backend in ('conference', 'wazo'):
            verify_certificate = resource[config_name]['confd'].get('verify_certificate')
            if verify_certificate in (True, False):
                verify = verify_certificate
            else:
                verify = True
                resource[config_name]['confd']['certificate_path'] = verify_certificate

            resource[config_name]['confd']['verify_certificate'] = verify

        form = self.form(data=resource)
        return form

    def _get_template(self, type_=None, backend=None):
        blueprint = request.blueprint.replace('.', '/')

        if not type_:
            return '{blueprint}/form/form_{backend}.html'.format(
                blueprint=blueprint,
                backend=backend
            )
        else:
            return '{blueprint}/{type_}.html'.format(
                blueprint=blueprint,
                type_=type_
            )


class DirdSourceListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        sources = self.service.list()
        results = [{'id': source['uuid'], 'text': source['name']} for source in sources['items']]
        return jsonify(build_select2_response(results, sources['total'], params))
