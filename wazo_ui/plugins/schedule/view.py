# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ScheduleForm


class ScheduleView(BaseIPBXHelperView):
    form = ScheduleForm
    resource = 'schedule'

    @menu_item(
        '.ipbx.call_management.schedules',
        l_('Schedules'),
        icon='clock-o',
        multi_tenant=True,
    )
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

    def _populate_form(self, form):
        form.timezone.choices = self._build_set_choices_timezones(form)
        return form

    def _build_set_choices_timezones(self, form):
        if not form.timezone.data or form.timezone.data == 'None':
            return []
        return [(form.timezone.data, form.timezone.data)]

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('schedule', {}))
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = form.to_dict()
        if form_id:
            resource['id'] = form_id
        resource['timezone'] = form.timezone.data or None
        return resource


class ScheduleListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        schedules = self.service.list(**params)
        results = [
            {'id': schedule['id'], 'text': schedule['name']}
            for schedule in schedules['items']
        ]
        return jsonify(build_select2_response(results, schedules['total'], params))
