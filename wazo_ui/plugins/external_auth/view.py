# Copyright 2018-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import request, redirect, url_for, render_template, flash
from flask_classful import route
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ExternalAuthForm


class ExternalAuthView(BaseIPBXHelperView):
    form = ExternalAuthForm
    resource = 'external_auth'

    @menu_item('.ipbx.identity.external_auth', l_('External Auth'), icon='external-link', multi_tenant=True)
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
            backend_list = self.service.list_backend()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))

        form = form or self.form()
        form = self._populate_form(form)

        for item in resource_list['items']:
            item['uuid'] = item['type']

        configured_types = [service['type'] for service in resource_list['items']]

        type_list = [service_type for service_type in backend_list if service_type not in configured_types]

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=resource_list,
                               type_list=type_list,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               listing_urls=self.listing_urls)

    @route('/new/<type>', methods=['GET'])
    def new(self, type):
        form = self.form(type=type, editing=False)

        return render_template(self._get_template(type=type),
                               form_mode='add',
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               form=form)

    def _get(self, type, form=None):
        try:
            resource = self.service.get(type)
            resource['type'] = type
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        form = form or self._map_resources_to_form(resource)
        form = self._populate_form(form)

        return render_template(self._get_template(type=resource['type']),
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
            if resources['editing'] == 'True':
                self.service.update(resources, form)
            else:
                self.service.create(resources, form)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._new(form)

        flash('Resource has been created', 'success')
        return self._redirect_for('index')

    def _map_resources_to_form(self, resource):
        type = resource['type']
        config_name = type + '_config'
        resource[config_name] = resource

        form = self.form(data=resource, editing=True)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)

        if 'mobile_config' in resource:
            resource['mobile_config']['is_sandbox'] = 'is_sandbox' in resource['mobile_config']

        return resource

    def _get_template(self, type_=None, type=None):
        blueprint = request.blueprint.replace('.', '/')

        if not type_:
            return '{blueprint}/form/form_{type}.html'.format(
                blueprint=blueprint,
                type=type
            )
        else:
            return '{blueprint}/{type_}.html'.format(
                blueprint=blueprint,
                type_=type_
            )
