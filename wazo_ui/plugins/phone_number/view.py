# Copyright 2024-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import jsonify, request
from flask_babel import lazy_gettext as l_
from flask_classful import route

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import PhoneNumberForm


class PhoneNumberView(BaseIPBXHelperView):
    form = PhoneNumberForm
    resource = 'phone_number'

    @menu_item(
        '.ipbx.call_management.phone_numbers',
        l_('Phone Numbers'),
        icon="long-arrow-right",
        order=2,
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _populate_form(self, form):
        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        if data.get('hidden_main') != 'False':
            data['shared'] = True
        if form_id:
            try:
                data['id'] = int(form_id)
            except ValueError:
                data['uuid'] = form_id
        return data

    def _map_resources_to_form(self, resource):
        resource['hidden_main'] = resource['main']
        form = self.form(data=resource)
        return form

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('phone_number', {}))
        return form

    @route('/select_main_number/', methods=['POST'])
    def select_main_number(self):
        body = request.get_json(force=True)
        self.service.select_main_number(body['number_uuid'])
        return jsonify(body)
