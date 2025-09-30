# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from flask_classful import route
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import (
    ConfBridgeGeneralSettingsForm,
    FeaturesGeneralSettingsForm,
    IaxGeneralSettingsForm,
    PJSIPGlobalSettingsForm,
    PJSIPSystemSettingsForm,
    SCCPGeneralSettingsForm,
    VoicemailGeneralSettingsForm,
)

logger = logging.getLogger(__name__)


class BaseGeneralSettingsView(BaseIPBXHelperView):
    settings = None

    def index(self, form=None):
        try:
            resource = self.service.get()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        form = form or self._map_resources_to_form(resource)
        form = self._populate_form(form)

        kwargs = {'form': form}
        if self.listing_urls:
            kwargs['listing_urls'] = self.listing_urls
        return render_template(self._get_template(self.settings), **kwargs)

    @route('/put', methods=['POST'])
    def put(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self.index(form)

        resources = self._map_form_to_resources(form)
        try:
            self.service.update(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self.index(form)

        flash(
            _('%(resource)s: Resource has been updated', resource=self.resource),
            'success',
        )
        return self._redirect_for('index')

    def _map_resources_to_form(self, resource):
        resource['options'] = self._build_options(resource['options'])
        form = self.form(data=resource)
        return form

    def _build_options(self, options):
        return [
            {'option_key': option_key, 'option_value': option_value}
            for option_key, option_value in options.items()
        ]

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['options'] = self._map_options_to_resource(data['options'])
        return data

    def _map_options_to_resource(self, options):
        return {option['option_key']: option['option_value'] for option in options}


class BasePJSIPSettingsView(BaseGeneralSettingsView):
    def _map_form_to_resources(self, form, form_id=None):
        raw = form.to_dict()['options']
        return {
            'options': {option['option_key']: option['option_value'] for option in raw},
        }

    def _map_resources_to_form(self, resource):
        options = [
            {'option_key': key, 'option_value': value}
            for key, value in resource['options'].items()
        ]
        choices = [(key, key) for key in resource['options'].keys()]
        form = self.form(data={'options': options})

        # Use all the current options for the choices, the complete list will be pulled on edit
        for option in form.options:
            option.option_key.choices = choices

        return form


class PJSIPGlobalSettingsView(BasePJSIPSettingsView):
    form = PJSIPGlobalSettingsForm
    resource = 'pjsip_global_settings'
    settings = 'pjsip_global'

    @menu_item(
        '.ipbx.global_settings.pjsip_global_settings',
        l_('PJSIP Global Settings'),
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)


class PJSIPSystemSettingsView(BasePJSIPSettingsView):
    form = PJSIPSystemSettingsForm
    resource = 'pjsip_system_settings'
    settings = 'pjsip_system'

    @menu_item(
        '.ipbx.global_settings.pjsip_system_settings',
        l_('PJSIP System Settings'),
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)


class IaxGeneralSettingsView(BaseGeneralSettingsView):
    form = IaxGeneralSettingsForm
    resource = 'iax_general_settings'
    settings = 'iax_general'

    @menu_item(
        '.ipbx.global_settings.iax_general_settings',
        l_('IAX'),
        order=5,
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_resources_to_form(self, resource):
        resource['general']['options'] = self._build_options(
            resource['general']['options']
        )
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['general']['options'] = self._map_options_to_resource(
            data['general']['options']
        )
        return data


class SCCPGeneralSettingsView(BaseGeneralSettingsView):
    form = SCCPGeneralSettingsForm
    resource = 'sccp_general_settings'
    settings = 'sccp_general'

    @menu_item(
        '.ipbx.global_settings.sccp_general_settings',
        l_('SCCP'),
        order=6,
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)


class VoicemailGeneralSettingsView(BaseGeneralSettingsView):
    form = VoicemailGeneralSettingsForm
    resource = 'voicemail_general_settings'
    settings = 'voicemail_general'

    @menu_item(
        '.ipbx.global_settings.voicemail_general_settings',
        l_('Voicemail'),
        order=7,
        icon='envelope',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_resources_to_form(self, resource):
        resource['general']['options'] = self._build_options(
            resource['general']['options']
        )
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        for zonemessage in form.zonemessages:
            zonemessage.timezone.choices = self._build_set_choices_timezones(
                zonemessage
            )
        return form

    def _build_set_choices_timezones(self, zonemessage):
        if not zonemessage.timezone.data:
            return []
        return [(zonemessage.timezone.data, zonemessage.timezone.data)]

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['general']['options'] = self._map_options_to_resource(
            data['general']['options']
        )
        return data


class FeaturesGeneralSettingsView(BaseGeneralSettingsView):
    form = FeaturesGeneralSettingsForm
    resource = 'features_general_settings'
    settings = 'features_general'

    @menu_item(
        '.ipbx.global_settings.features_general_settings',
        l_('Features Code'),
        order=8,
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_resources_to_form(self, resource):
        resource['general']['options'] = self._build_options(
            resource['general']['options']
        )
        resource['featuremap']['options'] = self._build_options(
            resource['featuremap']['options']
        )
        resource['applicationmap']['options'] = self._build_options(
            resource['applicationmap']['options']
        )
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['general']['options'] = self._map_options_to_resource(
            data['general']['options']
        )
        data['featuremap']['options'] = self._map_options_to_resource(
            data['featuremap']['options']
        )
        data['applicationmap']['options'] = self._map_options_to_resource(
            data['applicationmap']['options']
        )
        return data


class ConfBridgeGeneralSettingsView(BaseGeneralSettingsView):
    form = ConfBridgeGeneralSettingsForm
    resource = 'confbridge_general_settings'
    settings = 'confbridge_general'

    @menu_item(
        '.ipbx.global_settings.confbridge_general_settings',
        l_('Conference'),
        order=9,
        icon='compress',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_resources_to_form(self, resource):
        resource['wazo_default_user']['options'] = self._build_options(
            resource['wazo_default_user']['options']
        )
        resource['wazo_default_bridge']['options'] = self._build_options(
            resource['wazo_default_bridge']['options']
        )
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['wazo_default_user']['options'] = self._map_options_to_resource(
            data['wazo_default_user']['options']
        )
        data['wazo_default_bridge']['options'] = self._map_options_to_resource(
            data['wazo_default_bridge']['options']
        )
        return data


class SCCPDocListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        doc = self.service.get()
        term = params.get('search') or ''
        with_id = [item for item in doc if term in item['text']]
        params['limit'] = len(with_id)  # avoid pagination
        return jsonify(build_select2_response(with_id, len(with_id), params))


class PJSIPDocListingView(LoginRequiredView):
    def list_json_by_section(self, section):
        params = extract_select2_params(request.args)
        doc = self.service.get().get(section, {}).keys()
        term = params.get('search') or ''
        with_id = [{'id': key, 'text': key} for key in doc if term in key]
        params['limit'] = len(with_id)  # avoid pagination
        return jsonify(build_select2_response(with_id, len(with_id), params))


class TimezoneListingView(LoginRequiredView):
    def list_json(self):
        params = extract_select2_params(request.args)
        timezones = self.service.list_timezones()['items']
        term = params.get('search') or ''
        results = []
        for tz in timezones:
            if term and term.lower() not in tz['zone_name'].lower():
                continue
            results.append({'id': tz['zone_name'], 'text': tz['zone_name']})
        params['limit'] = len(results)  # avoid pagination
        return jsonify(build_select2_response(results, len(results), params))
