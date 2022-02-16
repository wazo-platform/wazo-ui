# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import (
    jsonify,
    request,
    flash,
    redirect,
    render_template,
    url_for
)
from flask_babel import (
    gettext as _,
    lazy_gettext as l_
)
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import DeviceForm


class DeviceView(BaseIPBXHelperView):
    form = DeviceForm
    resource = 'device'

    @menu_item('.ipbx.user_management.devices', l_('Devices'), order=4, icon="phone-square", multi_tenant=True)
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            device_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))

        try:
            unallocated_list = self.service.list_unallocated()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))

        # We do not want the unallocated devices to be editable
        for device in unallocated_list['items']:
            device['editable'] = False

        form = form or self.form()
        form = self._populate_form(form)

        resources = {'all': device_list, 'unallocated': unallocated_list}

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=resources,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               listing_urls=self.listing_urls)

    def _populate_form(self, form):
        form.plugin.choices = self._build_set_choices_plugin(form)
        form.template_id.choices = self._build_set_choices_template_id(form)
        return form

    def _build_set_choices_plugin(self, device):
        if not device.plugin.data or device.plugin.data == 'None':
            return []
        return [(device.plugin.data, device.plugin.data)]

    def _build_set_choices_template_id(self, device):
        if not device.template_id.data or device.template_id.data == 'None':
            return []
        template_id = self.service.get_config(device.template_id.data)
        if template_id:
            return [(template_id['id'], template_id['label'])]
        return [(device.template_id.data, device.template_id.data)]

    def autoprov(self, device_id):
        try:
            self.service.autoprov(device_id)
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        flash(_('%(resource)s: Resource has been reset to autoprov', resource=self.resource), 'success')
        return self._redirect_for('index')

    def synchronize(self, device_id):
        try:
            self.service.synchronize(device_id)
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        flash(_('%(resource)s: Resource has been synchronized', resource=self.resource), 'success')
        return self._redirect_for('index')

    def assign_tenant(self, device_id):
        try:
            self.service.assign_tenant(device_id)
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        flash(_('%(resource)s: Device has been assigned to tenant', resource=self.resource), 'success')
        return self._redirect_for('index')


class DeviceListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        devices = self.service.list(**params)
        results = [{'id': device['id'], 'text': device['mac']} for device in devices['items']]
        return jsonify(build_select2_response(results, devices['total'], params))
