# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from flask import jsonify, request, render_template

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import TrunkForm


class TrunkView(BaseIPBXHelperView):
    form = TrunkForm
    resource = 'trunk'

    @menu_item('.ipbx.trunks', l_('Trunks'), icon="server", multi_tenant=True)
    def index(self):
        return super().index()

    def new(self, protocol):
        if protocol not in ['sip', 'iax', 'custom']:
            return self._index()

        return render_template(self._get_template('protocol_{}'.format(protocol)),
                               form=self.form(),
                               listing_urls=self.listing_urls)

    def _map_resources_to_form(self, resource):
        if resource['endpoint_sip']:
            resource['protocol'] = 'sip'
            endpoint_sip = self.service.get_endpoint_sip(resource['endpoint_sip']['id'])
            self._build_host_for_endpoint(endpoint_sip)
            endpoint_sip['options'] = self._build_sip_iax_options(endpoint_sip['options'])
            if resource['register_sip']:
                resource['register_sip'] = self.service.get_register_sip(resource['register_sip']['id'])
            resource['endpoint_sip'] = endpoint_sip
        elif resource['endpoint_iax']:
            resource['protocol'] = 'iax'
            endpoint_iax = self.service.get_endpoint_iax(resource['endpoint_iax']['id'])
            self._build_host_for_endpoint(endpoint_iax)
            endpoint_iax['options'] = self._build_sip_iax_options(endpoint_iax['options'])
            if resource['register_iax']:
                resource['register_iax'] = self.service.get_register_iax(resource['register_iax']['id'])
            resource['endpoint_iax'] = endpoint_iax
        elif resource['endpoint_custom']:
            resource['protocol'] = 'custom'
            endpoint_custom = self.service.get_endpoint_custom(resource['endpoint_custom']['id'])
            resource['endpoint_custom'] = endpoint_custom

        form = self.form(data=resource)
        return form

    def _build_host_for_endpoint(self, endpoint):
        if endpoint['host'] != 'dynamic':
            endpoint['host_value'] = endpoint['host']
            endpoint['host'] = 'static'

    def _build_sip_iax_options(self, options):
        return [{'option_key': option[0], 'option_value': option[1]} for option in options]

    def _populate_form(self, form):
        form.context.choices = self._build_set_choices_context(form.context)
        return form

    def _build_set_choices_context(self, context_form):
        if not context_form.data or context_form.data == 'None':
            return []

        context = self.service.get_context(context_form.data)
        if context:
            return [(context['name'], context['label'])]

        return [(context_form.data, context_form.data)]

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('trunk', {}))
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        if 'username' in resource['endpoint_sip']:
            resource['endpoint_sip'] = self._map_form_to_resource_endpoint(resource['endpoint_sip'])
            del resource['endpoint_custom'], resource['endpoint_iax'], resource['register_iax']
            if (not resource['register_sip']['enabled']
                    and not resource['register_sip']['remote_host']
                    and not resource['register_sip']['sip_username']):
                resource['register_sip'] = None

        elif 'name' in resource['endpoint_iax']:
            resource['endpoint_iax'] = self._map_form_to_resource_endpoint(resource['endpoint_iax'])
            del resource['endpoint_custom'], resource['endpoint_sip'], resource['register_sip']
            if (not resource['register_iax']['enabled']
                    and not resource['register_iax']['remote_host']):
                resource['register_iax'] = None

        elif 'interface' in resource['endpoint_custom']:
            del resource['endpoint_sip'], resource['endpoint_iax'], resource['register_sip'], resource['register_iax']

        return resource

    def _map_form_to_resource_endpoint(self, endpoint):
        if endpoint['host'] == 'static':
            endpoint['host'] = endpoint.pop('host_value')

        endpoint['options'] = [[option['option_key'], option['option_value']] for option in endpoint['options']]
        return endpoint


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
                text = '{} ({})'.format(trunk['endpoint_sip']['username'], 'sip')
            if trunk.get('endpoint_iax'):
                text = '{} ({})'.format(trunk['endpoint_iax']['name'], 'iax')
            results.append({'id': trunk['id'], 'text': text})
        return results
