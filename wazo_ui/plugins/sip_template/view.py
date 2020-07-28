# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView, NewHelperViewMixin

from .form import EndpointSIPTemplateForm

SECTIONS = [
    'aor_section_options',
    'auth_section_options',
    'endpoint_section_options',
    'identify_section_options',
    'registration_section_options',
    'registration_outbound_auth_section_options',
    'outbound_auth_section_options',
]

EXCLUDE_CHOICE_SECTIONS = [
    'identify_section_options',
    'registration_section_options',
]


class EndpointSIPTemplateView(NewHelperViewMixin, BaseIPBXHelperView):

    form = EndpointSIPTemplateForm
    resource = l_('SIP Template')

    @menu_item('.ipbx.sip_templates', l_('SIP Templates'), icon="compress", multi_tenant=True)
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.transport.form.uuid.choices = self._build_set_choices_transport(form)
        return form

    def _build_set_choices_transport(self, template):
        transport_uuid = template.transport.form.uuid.data
        if not transport_uuid or transport_uuid == 'None':
            return []
        transport = self.service.get_transport(transport_uuid)
        return [(transport['uuid'], transport['name'])]

    def _map_resources_to_form(self, resource):
        choices = []
        for section in SECTIONS:
            for key, _ in resource[section]:
                choices.append((key, key))

            resource[section] = self._build_options(resource[section])

        form = self.form(data=resource)

        for section in SECTIONS:
            if section in EXCLUDE_CHOICE_SECTIONS:
                continue

            for option in getattr(form, section):
                option.option_key.choices = choices

        return form

    def _build_options(self, options):
        return [
            {'option_key': option_key, 'option_value': option_value}
            for option_key, option_value in options
        ]

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        if form_id:
            data['uuid'] = form_id

        for section in SECTIONS:
            data[section] = self._map_options_to_resource(data[section])

        if not data['transport'].get('uuid'):
            data['transport'] = None

        return data

    def _map_options_to_resource(self, options):
        return [[option['option_key'], option['option_value']] for option in options]
