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

from .form import QueueForm


class QueueView(BaseIPBXHelperView):
    form = QueueForm
    resource = 'queue'

    @menu_item('.ipbx.callcenter', l_('Call Center'), icon="support", multi_tenant=True)
    @menu_item('.ipbx.callcenter.queues', l_('Queues'), icon="cubes", multi_tenant=True)
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
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(
            form.schedules[0]
        )
        form.members.agent_ids.choices = self._build_set_choices_agents(
            form.members.agents
        )
        form.members.user_ids.choices = self._build_set_choices_users(
            form.members.users
        )
        return form

    def _build_set_choices_agents(self, agents):
        return [(agent.form.id.data, agent.form.number.data) for agent in agents]

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = f'{user.firstname.data} {user.lastname.data}'
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

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

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

    def _map_resources_to_form(self, resource):
        resource['options'] = self._build_options(resource['options'])
        resource['members']['agent_ids'] = [
            agent['id'] for agent in resource['members']['agents']
        ]
        resource['members']['user_ids'] = [
            user['uuid'] for user in resource['members']['users']
        ]
        resource['fallbacks'] = self.service.get_fallbacks(resource['id'])
        form = self.form(data=resource)
        return form

    def _build_options(self, options):
        result = []
        for option in options:
            result.append({'option_key': option[0], 'option_value': option[1]})

        return result

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['options'] = self._map_form_to_resource_options(form, resource)
        resource['agents'] = [
            {'id': agent_id} for agent_id in resource['members']['agent_ids']
        ]
        resource['users'] = [
            {'id': user_id} for user_id in resource['members']['user_ids']
        ]
        resource['music_on_hold'] = self._convert_empty_string_to_none(
            form.music_on_hold.data
        )

        return resource

    def _map_form_to_resource_options(self, form, resource):
        options = []
        for option in resource['options']:
            options.append([option['option_key'], option['option_value']])

        return options

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('queue', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form


class QueueDestinationView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        queues = self.service.list(**params)
        results = [
            {'id': queue['id'], 'text': queue['name']} for queue in queues['items']
        ]
        return jsonify(build_select2_response(results, queues['total'], params))
