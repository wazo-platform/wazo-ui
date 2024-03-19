# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from flask_classful import route
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ConfigDeviceForm, ConfigRegistrarForm, ConfigurationForm


class ProvisioningBaseView(BaseIPBXHelperView):
    def _get_template(self, type_):
        blueprint = request.blueprint.replace('.', '/')
        return self.templates.get(
            type_,
            f'{blueprint}/{self.resource}/{type_}.html',
        )


class PluginView(ProvisioningBaseView):
    resource = 'plugin'

    @menu_item(
        '.ipbx.global_settings.provisioning_plugins',
        l_('Devices Plugins'),
        order=1,
        icon="file-code",
    )
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            self.service.update()
            plugins_installable = self.service.list_installable()
            plugins_installed = self.service.list_installed()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:get'))

        plugin_ids_installed = [p['id'] for p in plugins_installed['items']]

        for plugin_installable in plugins_installable['items']:
            if plugin_installable['id'] in plugin_ids_installed:
                plugin_installable['editable'] = True
            else:
                plugin_installable['editable'] = False

        return render_template(
            self._get_template('list'),
            resource_list=plugins_installable,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    def _get(self, id, form=None):
        try:
            plugin = self.service.get(id)
            packages_installable = self.service.get_packages_installable(id)
            packages_installed = self.service.get_packages_installed(id)
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        package_ids_installed = [p['id'] for p in packages_installed['items']]

        return render_template(
            self._get_template('edit'),
            plugin_name=id,
            plugin=plugin,
            resource_list=packages_installable,
            package_ids_installed=package_ids_installed,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    def install(self, plugin_name):
        try:
            self.service.install(plugin_name)
        except HTTPError as error:
            self._flash_http_error(error)
        else:
            flash(
                _('Plugin %(plugin_name)s has been installed', plugin_name=plugin_name),
                'success',
            )
        return redirect(url_for('.PluginView:index'))

    def uninstall(self, plugin_name):
        try:
            self.service.uninstall(plugin_name)
        except HTTPError as error:
            self._flash_http_error(error)
        else:
            flash(
                _(
                    'Plugin %(plugin_name)s has been uninstalled',
                    plugin_name=plugin_name,
                ),
                'success',
            )
        return redirect(url_for('.PluginView:index'))

    def install_package_ajax(self, plugin_name, package_name):
        try:
            result = self.service.install_package(plugin_name, package_name)
            return jsonify(state=result.state, location=result._location)
        except HTTPError as error:
            self._flash_http_error(error)
            return jsonify(error=error)

    def get_operation_status(self):
        location = request.args.get('location')
        result = self.service.get_package_status(location)

        return jsonify(
            state=result.state,
            base_url=result._command.base_url,
            location=result._location,
        )

    def uninstall_package_ajax(self, plugin_name, package_name):
        try:
            self.service.uninstall_package(plugin_name, package_name)
        except HTTPError as error:
            self._flash_http_error(error)
            return jsonify(error=error)
        else:
            flash(
                _(
                    'Package %(package_name)s has been uninstalled',
                    package_name=package_name,
                ),
                'success',
            )

        return jsonify(state='completed')


class PluginListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        plugins = self.service.list_installed(**params)
        results = [
            {'id': plugin['id'], 'text': plugin['id']} for plugin in plugins['items']
        ]
        results = sorted(results, key=lambda value: value['id'])
        offset = params['offset']
        limit = params['limit']
        results = results[offset : offset + limit]
        return jsonify(build_select2_response(results, plugins['total'], params))


class ConfigRegistrarView(ProvisioningBaseView):
    form = ConfigRegistrarForm
    resource = 'config_registrar'

    @menu_item(
        '.ipbx.global_settings.provisioning_configs',
        l_('Provisioning Registrars'),
        order=2,
        icon="file",
    )
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:get'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(
            self._get_template('list'),
            form=form,
            resource_list=resource_list,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )


class ConfigDeviceView(ProvisioningBaseView):
    form = ConfigDeviceForm
    resource = 'config_device'

    @menu_item(
        '.ipbx.global_settings.provisioning_devices',
        l_('Provisioning Config device'),
        order=3,
        icon="file-archive",
    )
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list_device()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:get'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(
            self._get_template('list'),
            form=form,
            resource_list=resource_list,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    def _populate_form(self, form):
        form.raw_config.timezone.choices = self._build_set_choices_timezones(
            form.raw_config
        )
        return form

    def _build_set_choices_timezones(self, config):
        if not config.timezone.data or config.timezone.data == 'None':
            return []
        return [(config.timezone.data, config.timezone.data)]

    def _map_form_to_resources(self, form, form_id=None):
        resource = form.to_dict()
        if form_id:
            resource['uuid'] = form_id
        resource['raw_config']['timezone'] = form.raw_config.timezone.data or None
        return resource


class ConfigurationView(ProvisioningBaseView):
    form = ConfigurationForm
    resource = 'configuration'

    @menu_item(
        '.ipbx.global_settings.provisioning_configuration',
        l_('Provisioning Configuration'),
        order=4,
        icon="cogs",
    )
    def index(self):
        return super().index()

    def _index(self, form=None):
        form = form or self.form()
        form = self._populate_form(form)

        return render_template(
            self._get_template('edit'),
            form=form,
            current_breadcrumbs=self._get_current_breadcrumbs(),
        )

    def _populate_form(self, form):
        return self.form(data=self.service.get())

    def _map_resources_to_form(self, resource):
        if resource['general_config']['NAT'] == '1':
            resource['general_config']['NAT'] = True
        else:
            resource['general_config']['NAT'] = False
        return self.form(data=resource)

    def _map_form_to_resources(self, form):
        data = form.to_dict()
        print(data)
        if 'NAT' in data['general_config']:
            data['general_config']['NAT'] = '1'
        else:
            data['general_config']['NAT'] = '0'
        return data

    @route('/put', methods=['POST'])
    def put(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._index(form)

        resources = self._map_form_to_resources(form)
        try:
            self.service.update(resources)
        except HTTPError as error:
            # provd does not return JSON errors
            self._flash_basic_form_errors(form)
            flash(_('Error during update: %(error)s', error=error), 'error')
            return self._index(form)

        flash(
            _('%(resource)s: Resource has been updated', resource=self.resource),
            'success',
        )
        return self._redirect_for('index')


class ConfigDeviceListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        configs = self.service.list_device(**params)
        results = [
            {'id': config['id'], 'text': config['label']} for config in configs['items']
        ]
        return jsonify(build_select2_response(results, configs['total'], params))


class ConfigRegistrarListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        registrars = self.service.list()
        results = []
        for registrar in registrars['items']:
            results.append({'id': registrar['id'], 'text': registrar['name']})

        return jsonify(build_select2_response(results, registrars['total'], params))
