# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ScheduleForm


class ScheduleView(BaseIPBXHelperView):
    form = ScheduleForm
    resource = 'schedule'

    @menu_item('.ipbx.schedules', l_('Schedules'), icon='clock-o', multi_tenant=True)
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        self._build_sound_destination(resource['closed_destination'])
        for exceptional_period in resource['exceptional_periods']:
            self._build_sound_destination(exceptional_period['destination'])
        form = self.form(data=resource)
        return form

    def _build_sound_destination(self, destination):
        if destination['type'] != 'sound':
            return
        file_, format_ = self.service.find_sound_by_path(destination['filename'])
        if file_:
            destination['name'] = file_['name']
            destination['format'] = format_['format']
            destination['language'] = format_['language']

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('schedule', {}))
        return form


class ScheduleListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        schedules = self.service.list(**params)
        results = [{'id': schedule['id'], 'text': schedule['name']} for schedule in schedules['items']]
        return jsonify(build_select2_response(results, schedules['total'], params))
