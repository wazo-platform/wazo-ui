# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask import jsonify, request

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView, NewHelperViewMixin

from .form import TransportForm

logger = logging.getLogger(__name__)


class TransportView(NewHelperViewMixin, BaseIPBXHelperView):
    form = TransportForm
    resource = 'transport'

    @menu_item('.ipbx.global_settings.transports', l_('PJSIP Transports'), icon="asterisk", multi_tenant=False)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        options = [{
            'option_key': option[0],
            'option_value': option[1],
        } for option in resource['options']]
        choices = [(key, key) for key, _ in resource['options']]

        form = self.form(
            id=resource['uuid'],
            data=resource,
            name=resource['name'],
            options=options,
        )

        # Use all the current options for the choices, the complete list will be pulled on edit
        for option in form.options:
            option.option_key.choices = choices

        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = super()._map_form_to_resources(form, form_id)
        data['options'] = [[opt['option_key'], opt['option_value']] for opt in data['options']]
        return data


class TransportDestinationView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        transports = self.service.list(**params)
        results = [{'id': t['uuid'], 'text': t['name']} for t in transports['items']]
        return jsonify(build_select2_response(results, transports['total'], params))
