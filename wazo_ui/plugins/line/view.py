# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import flash, jsonify, render_template, request
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView
from wazo_ui.plugins.sip_template.view import EXCLUDE_CHOICE_SECTIONS, SECTIONS

from .form import LineForm


class LineView(BaseIPBXHelperView):
    form = LineForm
    resource = 'line'

    @menu_item(
        '.ipbx.user_management.lines',
        l_('Lines'),
        order=3,
        icon="exchange",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def new(self, protocol):
        if protocol not in ['sip', 'sccp', 'custom']:
            return self._index()

        return render_template(
            self._get_template(f'protocol_{protocol}'),
            form=self.form(),
            listing_urls=self.listing_urls,
        )

    def post(self):
        form = self.form()
        resources = self._map_form_to_resources_post(form)

        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._new(form)

        try:
            self.service.create(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._new(form)

        flash(
            l_('%(resource)s: Resource has been created', resource=self.resource),
            'success',
        )
        return self._redirect_for('index')

    def _map_resources_to_form(self, resource):
        endpoint_sip = endpoint_sccp = endpoint_custom = protocol = None
        if resource['endpoint_sip']:
            protocol = 'sip'
            endpoint_sip = self.service.get_endpoint_sip(
                resource['endpoint_sip']['uuid']
            )

            choices = []
            for section in SECTIONS:
                for key, _ in endpoint_sip[section]:
                    choices.append((key, key))

                endpoint_sip[section] = self._build_options(endpoint_sip[section])

            endpoint_sip['template_uuids'] = [
                template['uuid'] for template in endpoint_sip['templates']
            ]

        elif resource['endpoint_sccp']:
            protocol = 'sccp'
            endpoint_sccp = self.service.get_endpoint_sccp(
                resource['endpoint_sccp']['id']
            )
            choices = []
            for key, _ in endpoint_sccp['options']:
                choices.append((key, key))
            endpoint_sccp['options'] = self._build_options(endpoint_sccp['options'])

        elif resource['endpoint_custom']:
            protocol = 'custom'
            endpoint_custom = self.service.get_endpoint_custom(
                resource['endpoint_custom']['id']
            )

        form = self.form(
            data=resource,
            protocol=protocol,
            endpoint_sip=endpoint_sip,
            endpoint_sccp=endpoint_sccp,
            endpoint_custom=endpoint_custom,
        )

        if resource['endpoint_sip']:
            for section in SECTIONS:
                if section in EXCLUDE_CHOICE_SECTIONS:
                    continue

                for option in getattr(form.endpoint_sip, section):
                    option.option_key.choices = choices

        if resource['endpoint_sccp']:
            for option in getattr(form.endpoint_sccp, 'options'):
                option.option_key.choices = choices

        return form

    def _build_options(self, options):
        return [
            {'option_key': option_key, 'option_value': option_value}
            for option_key, option_value in options
        ]

    def _populate_form(self, form):
        form.context.choices = self._build_set_choices_context(form.context)
        form.endpoint_sip.transport.form.uuid.choices = (
            self._build_set_choices_transport(form.endpoint_sip)
        )
        form.endpoint_sip.template_uuids.choices = self._build_set_choices_templates(
            form.endpoint_sip.templates
        )
        return form

    def _build_set_choices_context(self, context_form):
        if not context_form.data or context_form.data == 'None':
            return []

        context = self.service.get_context(context_form.data)
        if context:
            return [(context['name'], context['label'])]

        return [(context_form.data, context_form.data)]

    def _build_set_choices_transport(self, sip):
        transport_uuid = sip.transport.form.uuid.data
        if not transport_uuid or transport_uuid == 'None':
            return []
        transport = self.service.get_transport(transport_uuid)
        return [(transport['uuid'], transport['name'])]

    def _build_set_choices_templates(self, templates):
        results = []
        for template in templates:
            template = self.service.get_sip_template(template.uuid.data)
            results.append((template['uuid'], template['label']))
        return results

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('line', {}))
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        if not self._sip_is_empty(resource['endpoint_sip']):
            sip = resource['endpoint_sip']
            for section in SECTIONS:
                sip[section] = self._map_options_to_resource(sip[section])

            if not sip['transport'].get('uuid'):
                sip['transport'] = None

            template_uuids = form.endpoint_sip.template_uuids.data
            sip['templates'] = [
                {'uuid': template_uuid} for template_uuid in template_uuids
            ]

            resource['endpoint_custom'] = None
            resource['endpoint_sccp'] = None
        elif not self._sccp_is_empty(resource['endpoint_sccp']):
            options = self._map_options_to_resource(
                resource['endpoint_sccp']['options']
            )
            resource['endpoint_sccp']['options'] = options
            resource['endpoint_sip'] = None
            resource['endpoint_custom'] = None
        elif resource['endpoint_custom'] is not None:
            resource['endpoint_sip'] = None
            resource['endpoint_sccp'] = None

        return resource

    def _sip_is_empty(self, sip):
        empty = {
            'transport': {},
            'templates': [],
            **{section: [] for section in SECTIONS},
        }
        return sip == empty

    def _sccp_is_empty(self, sccp):
        empty = {'options': []}
        return sccp == empty

    def _map_options_to_resource(self, options):
        return [[option['option_key'], option['option_value']] for option in options]


class LineListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        lines = self.service.list(**params)
        results = self._populate_list(lines['items'])
        return jsonify(build_select2_response(results, lines['total'], params))

    def _populate_list(self, lines):
        results = []
        for line in lines:
            if line.get('endpoint_custom'):
                text = f'{line["endpoint_custom"]["interface"]} ({"custom"})'
            if line.get('endpoint_sccp'):
                text = f'{line["endpoint_sccp"]["id"]} ({"sccp"})'
            if line.get('endpoint_sip'):
                text = f'{line["endpoint_sip"]["label"]} ({"sip"})'
            results.append({'id': line['id'], 'text': text})
        return results
