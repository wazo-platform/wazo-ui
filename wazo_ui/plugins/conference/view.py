# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ConferenceForm


class ConferenceView(BaseIPBXHelperView):
    form = ConferenceForm
    resource = l_('conference')

    @menu_item('.ipbx.services', l_('Services'), icon="star", multi_tenant=True)
    @menu_item(
        '.ipbx.services.conferences',
        l_('Conferences'),
        icon="compress",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.extensions[0].exten.choices = self._build_set_choices_exten(
            form.extensions[0]
        )
        form.extensions[0].context.choices = self._build_set_choices_context(
            form.extensions[0]
        )
        form.music_on_hold.choices = self._build_set_choices_moh(form.music_on_hold)
        return form

    def _build_set_choices_exten(self, extension):
        if not extension.exten.data or extension.exten.data == 'None':
            return []
        return [(extension.exten.data, extension.exten.data)]

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            context = self.service.get_first_internal_context()
        else:
            context = self.service.get_context(extension.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(extension.context.data, extension.context.data)]

    def _build_set_choices_moh(self, moh):
        if not moh.data or moh.data == 'None':
            return []
        return [(moh.data, moh.data)]

    def _map_form_to_resources(self, form, form_id=None):
        resource = form.to_dict()
        if form_id:
            resource['uuid'] = form_id

        resource['music_on_hold'] = self._convert_empty_string_to_none(
            form.music_on_hold.data
        )

        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('conference', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form


class ConferenceDestinationView(LoginRequiredView):
    def list_json(self):
        return self._list_json('id')

    def uuid_list_json(self):
        return self._list_json('uuid')

    def _list_json(self, field_id):
        params = extract_select2_params(request.args)
        conferences = self.service.list(**params)
        results = []
        for conference in conferences['items']:
            text = '{}'.format(conference['name'])
            results.append({'id': conference[field_id], 'text': text})

        return jsonify(build_select2_response(results, conferences['total'], params))
