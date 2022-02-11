# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import request, jsonify

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)

from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ApplicationForm


class ApplicationView(BaseIPBXHelperView):
    form = ApplicationForm
    resource = 'application'

    @menu_item('.ipbx.services.applications', l_('Applications'), icon="cubes", multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        # TODO should be in the ApplicationDestinationForm
        destination = resource.pop('destination_options')
        destination['destination'] = resource.pop('destination') or 'None'
        form = self.form(data=resource, destination=destination)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        # TODO should be in the ApplicationDestinationForm
        resource = form.to_dict()
        if form_id:
            resource['uuid'] = form_id
        resource['destination_options'] = resource.pop('destination')
        resource['destination'] = resource['destination_options'].pop('destination')
        return resource


class ApplicationDestinationView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        applications = self.service.list()
        results = []
        for application in applications['items']:
            results.append({'id': application['uuid'], 'text': application['name']})

        return jsonify(build_select2_response(results, applications['total'], params))
