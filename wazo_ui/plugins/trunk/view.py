# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import jsonify, request, render_template, flash
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from wazo_ui.plugins.sip_template.view import SECTIONS, EXCLUDE_CHOICE_SECTIONS

from .form import TrunkForm


class TrunkView(BaseIPBXHelperView):
    form = TrunkForm
    resource = 'trunk'

    @menu_item('.ipbx.call_management.trunks', l_('Trunks'), icon="server", multi_tenant=True)
    def index(self):
        return super().index()

    def new(self, protocol):
        if protocol not in ['sip', 'iax', 'custom']:
            return self._index()

        return render_template(self._get_template('protocol_{}'.format(protocol)),
                               form=self.form(),
                               listing_urls=self.listing_urls)

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

        flash(l_('%(resource)s: Resource has been created', resource=self.resource), 'success')
        return self._redirect_for('index')

    def _map_resources_to_form(self, resource):
        if resource['endpoint_sip']:
            resource['protocol'] = 'sip'
            endpoint_sip = self.service.get_endpoint_sip(resource['endpoint_sip']['uuid'])
            choices = []
            for section in SECTIONS:
                for key, _ in endpoint_sip[section]:
                    choices.append((key, key))
                endpoint_sip[section] = self._build_options(endpoint_sip[section])
            endpoint_sip['template_uuids'] = [template['uuid'] for template in endpoint_sip['templates']]
            resource['endpoint_sip'] = endpoint_sip
        elif resource['endpoint_iax']:
            resource['protocol'] = 'iax'
            endpoint_iax = self.service.get_endpoint_iax(resource['endpoint_iax']['id'])
            self._build_host_for_endpoint(endpoint_iax)
            endpoint_iax['options'] = self._build_options(endpoint_iax['options'])
            if resource['register_iax']:
                resource['register_iax'] = self.service.get_register_iax(resource['register_iax']['id'])
            resource['endpoint_iax'] = endpoint_iax
        elif resource['endpoint_custom']:
            resource['protocol'] = 'custom'
            endpoint_custom = self.service.get_endpoint_custom(resource['endpoint_custom']['id'])
            resource['endpoint_custom'] = endpoint_custom

        form = self.form(data=resource)
        if resource['endpoint_sip']:
            for section in SECTIONS:
                if section in EXCLUDE_CHOICE_SECTIONS:
                    continue
                for option in getattr(form.endpoint_sip, section):
                    option.option_key.choices = choices

        return form

    def _build_host_for_endpoint(self, endpoint):
        if endpoint['host'] != 'dynamic':
            endpoint['host_value'] = endpoint['host']
            endpoint['host'] = 'static'

    def _build_options(self, options):
        return [
            {'option_key': option_key, 'option_value': option_value}
            for option_key, option_value in options
        ]

    def _populate_form(self, form):
        form.context.choices = self._build_set_choices_context(form.context)
        form.endpoint_sip.transport.form.uuid.choices = self._build_set_choices_transport(form.endpoint_sip)
        form.endpoint_sip.template_uuids.choices = self._build_set_choices_templates(form.endpoint_sip.templates)
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
        form.populate_errors(resources.get('trunk', {}))
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
            sip['templates'] = [{'uuid': template_uuid} for template_uuid in template_uuids]

            del resource['endpoint_custom'], resource['endpoint_iax'], resource['register_iax']
        elif not self._iax_is_empty(resource['endpoint_iax']):
            resource['endpoint_iax'] = self._map_form_to_resource_endpoint(resource['endpoint_iax'])
            del resource['endpoint_custom'], resource['endpoint_sip']
            if (not resource['register_iax']['enabled']
                    and not resource['register_iax']['remote_host']):
                resource['register_iax'] = None

        elif resource['endpoint_custom'] is not None:
            del resource['endpoint_sip'], resource['endpoint_iax'], resource['register_iax']

        return resource

    def _map_options_to_resource(self, options):
        return [[option['option_key'], option['option_value']] for option in options]

    def _map_form_to_resource_endpoint(self, endpoint):
        if endpoint['host'] == 'static':
            endpoint['host'] = endpoint.pop('host_value')

        endpoint['options'] = [[option['option_key'], option['option_value']] for option in endpoint['options']]
        return endpoint

    def _sip_is_empty(self, sip):
        empty = {
            'transport': {},
            'templates': [],
            **{section: [] for section in SECTIONS},
        }
        return sip == empty

    def _iax_is_empty(self, iax):
        empty = {'options': []}
        return iax == empty


class TrunkListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        trunks = self.service.list(**params)
        results = self._populate_list(trunks['items'])
        return jsonify(build_select2_response(results, trunks['total'], params))

    def _populate_list(self, trunks):
        results = []
        for trunk in trunks:
            if trunk.get('endpoint_custom'):
                text = '{} ({})'.format(trunk['endpoint_custom']['interface'], 'custom')
            if trunk.get('endpoint_sip'):
                text = '{} ({})'.format(trunk['endpoint_sip']['label'], 'sip')
            if trunk.get('endpoint_iax'):
                text = '{} ({})'.format(trunk['endpoint_iax']['name'], 'iax')
            results.append({'id': trunk['id'], 'text': text})
        return results
