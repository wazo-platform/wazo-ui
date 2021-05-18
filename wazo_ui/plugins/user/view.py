# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from random import randint

from flask import Response, request, jsonify, render_template, redirect, url_for, flash
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError
from flask_classful import route

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView, IndexAjaxHelperViewMixin

from .form import UserForm, ImportCSVForm


class UserView(IndexAjaxHelperViewMixin, BaseIPBXHelperView):
    form = UserForm
    import_csv_form = ImportCSVForm
    resource = 'user'

    @menu_item('.ipbx', l_('Telephony'), multi_tenant=True)
    @menu_item('.ipbx.user_management', l_('User Management'), order=1, icon="users", multi_tenant=True)
    @menu_item('.ipbx.user_management.users', l_('Users'), order=1, icon="user", multi_tenant=True)
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))

        form = self.form()
        form = self._populate_form(form)
        import_csv_form = self.import_csv_form()

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=resource_list,
                               import_csv_form=import_csv_form,
                               listing_urls=self.listing_urls)

    @route('/import_csv', methods=['POST'])
    def import_csv(self):
        form = self.import_csv_form()
        self.service.import_csv(form)

        flash('Resources have been imported', 'success')
        return self._redirect_for('index')

    def export_csv(self):
        content = self.service.export_csv()

        return Response(
            content,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=users.csv"})

    def update_csv(self):
        form = self.import_csv_form()
        self.service.update_csv(form)

        flash('Resources have been updated', 'success')
        return self._redirect_for('index')

    @route('/put/<id>', methods=['POST'])
    def put(self, id):
        super().put(id)
        return self._redirect_for('index')

    def _map_resources_to_form(self, resource):
        resource_lines = [self.service.get_line(line['id']) for line in resource['lines']]
        lines = self._build_lines(resource_lines)
        groups = [group['id'] for group in resource['groups']]
        resource_funckeys = self.service.list_funckeys(resource['uuid'])
        funckeys = self._build_funckeys(resource_funckeys)
        resource['call_permission_ids'] = [call_permission['id'] for call_permission in resource['call_permissions']]
        form = self.form(data=resource, lines=lines, group_ids=groups, funckeys=funckeys)
        return form

    def _build_funckeys(self, funckeys):
        keys = [dict(digit=digit, **key) for digit, key in funckeys['keys'].items()]
        keys.sort(key=lambda k: k['digit'])
        return keys

    def _populate_form(self, form):
        form.music_on_hold.choices = self._build_set_choices_moh(form)
        form.outgoing_caller_id.choices = self._build_set_choices_outgoing_caller_id(form)
        for form_line in form.lines:
            form_line.template_uuids.choices = self._build_set_choices_templates(form_line)
            form_line.application.form.uuid.choices = self._build_set_choices_application(form_line)
            form_line.registrar.choices = self._build_set_choices_registrar(form_line)
            form_line.device.choices = self._build_set_choices_device(form_line)
            form_line.context.choices = self._build_set_choices_context(form_line)
            for form_extension in form_line.extensions:
                form_extension.exten.choices = self._build_set_choices_extension(form_extension)
        form.group_ids.choices = self._build_set_choices_groups(form.groups)
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(form.schedules[0])
        form.voicemail.form.id.choices = self._build_set_choices_voicemail(form)
        form.call_permission_ids.choices = self._build_set_choices_callpermissions(form.call_permissions)
        return form

    def _build_set_choices_templates(self, line):
        results = []
        for template_uuid in line.template_uuids.data:
            template = self.service.get_sip_template(template_uuid)
            results.append((template['uuid'], template['label']))
        return results

    def _build_set_choices_application(self, line):
        application = line.application.form
        if not application.uuid.data or application.uuid.data == 'None':
            return []
        return [(application.uuid.data, application.name.data)]

    def _build_set_choices_registrar(self, line):
        if not line.registrar.data or line.registrar.data == 'None':
            return []
        registrar_name = self.service.get_registrar(line.registrar.data)['name']
        text = registrar_name if registrar_name else line.registrar.data
        return [(line.registrar.data, text)]

    def _build_set_choices_device(self, line):
        if not line.device.data or line.device.data == 'None':
            return []
        device_mac = self.service.get_device(line.device.data)['mac']
        text = device_mac if device_mac else line.device.data
        return [(line.device.data, text)]

    def _build_set_choices_context(self, line):
        if not line.context.data or line.context.data == 'None':
            context = self.service.get_first_internal_context()
        else:
            context = self.service.get_context(line.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(line.context.data, line.context.data)]

    def _build_set_choices_extension(self, extension):
        if not extension.exten.data or extension.exten.data == 'None':
            return []
        return [(extension.exten.data, extension.exten.data)]

    def _build_set_choices_moh(self, user):
        if not user.music_on_hold.data or user.music_on_hold.data == 'None':
            return []
        return [(user.music_on_hold.data, user.music_on_hold.data)]

    def _build_set_choices_outgoing_caller_id(self, user):
        choices = [
            ('default', l_('Default')),
            ('anonymous', l_('Anonymous'))
        ]
        caller_id = user.outgoing_caller_id.data
        if not caller_id or caller_id == 'None':
            return choices
        for choice in choices:
            if choice[0] == caller_id:
                return choices
        selected_choice = (caller_id, caller_id)
        choices.append(selected_choice)
        return choices

    def _build_set_choices_groups(self, groups):
        results = []
        for group in groups:
            results.append((group.form.id.data, group.form.name.data))
        return results

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

    def _build_set_choices_voicemail(self, user):
        if not user.voicemail.form.id.data or user.voicemail.form.id.data == 'None':
            return []
        return [(user.voicemail.form.id.data, user.voicemail.form.name.data)]

    def _build_set_choices_callpermissions(self, call_permissions):
        return [(call_permission.form.id.data, call_permission.form.name.data) for call_permission in call_permissions]

    def _build_lines(self, lines):
        results = []
        for line in lines:
            name = protocol = 'undefined'
            endpoint_sip_uuid = endpoint_sccp_id = endpoint_custom_id = ''
            template_uuids = []
            if line.get('endpoint_sip'):
                protocol = 'sip'
                endpoint_sip = self.service.get_endpoint_sip(line['endpoint_sip']['uuid'])
                name = endpoint_sip['name']
                template_uuids = [template['uuid'] for template in endpoint_sip['templates']]
                endpoint_sip_uuid = line['endpoint_sip']['uuid']
            elif line.get('endpoint_sccp'):
                protocol = 'sccp'
                name = line['extensions'][0]['exten'] if line['extensions'] else ''
                endpoint_sccp_id = line['endpoint_sccp']['id']
            elif line.get('endpoint_custom'):
                protocol = 'custom'
                name = line['endpoint_custom']['interface']
                endpoint_custom_id = line['endpoint_custom']['id']

            device = line['device_id'] if line['device_id'] else ''
            results.append({'protocol': protocol,
                            'template_uuids': template_uuids,
                            'name': name,
                            'device': device,
                            'position': line['position'],
                            'context': line['context'],
                            'id': line['id'],
                            'application': line.get('application'),
                            'registrar': line.get('registrar'),
                            'extensions': line['extensions'],
                            'endpoint_sip_uuid': endpoint_sip_uuid,
                            'endpoint_sccp_id': endpoint_sccp_id,
                            'endpoint_custom_id': endpoint_custom_id})
        return results

    def _map_form_to_resources_post(self, form):
        form.username.raw_data = form.email.raw_data
        form.username.data = form.email.data
        return self._map_form_to_resources(form)

    def _map_form_to_resources(self, form, form_id=None):
        resource = form.to_dict()
        if form_id:
            resource['uuid'] = form_id
        resource['groups'] = self._map_form_to_resource_group(form)
        resource['lines'] = self._map_form_to_resource_line(form)
        resource['funckeys'] = self._map_form_to_resource_funckey(form)
        resource['call_permissions'] = [{'id': call_permission_id} for call_permission_id in
                                        form.call_permission_ids.data]
        resource['music_on_hold'] = form.music_on_hold.data or None

        return resource

    def _map_form_to_resource_funckey(self, form):
        funckeys = {
            'keys': {}
        }
        for funckey in form.funckeys:
            funckey = funckey.to_dict()
            funckeys['keys'][funckey.pop('digit')] = funckey

        return funckeys

    def _map_form_to_resource_group(self, form):
        return [{'id': group_id} for group_id in form.group_ids.data]

    def _map_form_to_resource_line(self, form):
        lines = []
        for line in form.lines:
            line = line.to_dict()
            if request.method == 'POST' and not line.get('context'):
                continue
            result = {'id': int(line['id']) if line['id'] else None,
                      'context': line.get('context'),
                      'position': line['position'],
                      'device_id': line.get('device')}

            if line['protocol'] == 'sip':
                templates = [{'uuid': uuid} for uuid in line.get('template_uuids', [])]
                result['endpoint_sip'] = {'uuid': line['endpoint_sip_uuid'], 'templates': templates}
            elif line['protocol'] == 'sccp':
                result['endpoint_sccp'] = {'id': line['endpoint_sccp_id']}
            elif line['protocol'] == 'custom':
                result['endpoint_custom'] = {'id': line['endpoint_custom_id'],
                                             'interface': str(randint(0, 99999999))}  # TODO: to improve ...

            if line['extensions'][0].get('exten') and line.get('context'):
                result['extensions'] = [{'id': line['extensions'][0]['id'],
                                         'exten': line['extensions'][0]['exten'],
                                         'context': line['context']}]

            if line['application'].get('uuid'):
                result['application'] = line['application']

            if line.get('registrar'):
                result['registrar'] = line['registrar']

            lines.append(result)

        return lines

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('user', {}))
        return form


class UserDestinationView(LoginRequiredView):

    def list_json(self):
        return self._list_json('id')

    def uuid_list_json(self):
        return self._list_json('uuid')

    def _list_json(self, field_id):
        params = extract_select2_params(request.args)
        users = self.service.list(**params)
        results = []
        for user in users['items']:
            if user.get('lastname'):
                text = '{} {}'.format(user['firstname'], user['lastname'])
            else:
                text = user['firstname']

            results.append({'id': user[field_id], 'text': text})

        return jsonify(build_select2_response(results, users['total'], params))
