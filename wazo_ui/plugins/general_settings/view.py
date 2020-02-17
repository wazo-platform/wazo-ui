# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from flask import (
    flash,
    redirect,
    request,
    render_template,
    url_for,
    jsonify,
)
from flask_classful import route
from requests.exceptions import HTTPError

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView
from wazo_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)

from .form import (
    ConfBridgeGeneralSettingsForm,
    FeaturesGeneralSettingsForm,
    IaxGeneralSettingsForm,
    SccpGeneralSettingsForm,
    PJSIPGlobalSettingsForm,
    SipGeneralSettingsForm,
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

        flash(_('%(resource)s: Resource has been updated', resource=self.resource), 'success')
        return self._redirect_for('index')

    def _map_resources_to_form(self, resource):
        resource['options'] = self._build_options(resource['options'])
        form = self.form(data=resource)
        return form

    def _build_options(self, options):
        return [{'option_key': option_key, 'option_value': option_value} for option_key, option_value in
                options.items()]

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['options'] = self._map_options_to_resource(data['options'])
        return data

    def _map_options_to_resource(self, options):
        return {option['option_key']: option['option_value'] for option in options}


class PJSIPGlobalSettingsView(BaseGeneralSettingsView):
    form = PJSIPGlobalSettingsForm
    resource = 'pjsip_global_settings'
    settings = 'pjsip_global'

    @menu_item(
        '.ipbx.advanced.pjsip_global_settings',
        l_('PJSIP Global Settings'),
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_form_to_resources(self, form, form_id=None):
        raw = form.to_dict()['options']
        return {
            'options': {option['option_key']: option['option_value'] for option in raw},
        }

    def _map_resources_to_form(self, resource):
        logger.critical('resource: %s', resource)
        result = super()._map_resources_to_form(resource)
        logger.critical('result: %s', resource)
        return result


class SipGeneralSettingsView(BaseGeneralSettingsView):
    form = SipGeneralSettingsForm
    resource = 'sip_general_settings'
    settings = 'sip_general'

    @menu_item(
        '.ipbx.advanced.sip_general_settings',
        l_('SIP General Settings'),
        order=4,
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()

        data['ordered_options'] = [[option['option_key'], option['option_value']] for option in data['ordered_options']]
        data['ordered_options'] += [[option['option_key'], option['option_value']] for option in data['options']]

        data['options'] = {}
        return data


class IaxGeneralSettingsView(BaseGeneralSettingsView):
    form = IaxGeneralSettingsForm
    resource = 'iax_general_settings'
    settings = 'iax_general'

    @menu_item(
        '.ipbx.advanced.iax_general_settings',
        l_('IAX General Settings'),
        order=5,
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_resources_to_form(self, resource):
        resource['general']['options'] = self._build_options(resource['general']['options'])
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['general']['options'] = self._map_options_to_resource(data['general']['options'])
        return data


class SccpGeneralSettingsView(BaseGeneralSettingsView):
    form = SccpGeneralSettingsForm
    resource = 'sccp_general_settings'
    settings = 'sccp_general'

    @menu_item(
        '.ipbx.advanced.sccp_general_settings',
        l_('SCCP General Settings'),
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
        '.ipbx.advanced.voicemail_general_settings',
        l_('Voicemail General Settings'),
        order=7,
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_resources_to_form(self, resource):
        resource['general']['options'] = self._build_options(resource['general']['options'])
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['general']['options'] = self._map_options_to_resource(data['general']['options'])
        return data


class FeaturesGeneralSettingsView(BaseGeneralSettingsView):
    form = FeaturesGeneralSettingsForm
    resource = 'features_general_settings'
    settings = 'features_general'

    @menu_item(
        '.ipbx.advanced.features_general_settings',
        l_('Features General Settings'),
        order=8,
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_resources_to_form(self, resource):
        resource['general']['options'] = self._build_options(resource['general']['options'])
        resource['featuremap']['options'] = self._build_options(resource['featuremap']['options'])
        resource['applicationmap']['options'] = self._build_options(resource['applicationmap']['options'])
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['general']['options'] = self._map_options_to_resource(data['general']['options'])
        data['featuremap']['options'] = self._map_options_to_resource(data['featuremap']['options'])
        data['applicationmap']['options'] = self._map_options_to_resource(data['applicationmap']['options'])
        return data


class ConfBridgeGeneralSettingsView(BaseGeneralSettingsView):
    form = ConfBridgeGeneralSettingsForm
    resource = 'confbridge_general_settings'
    settings = 'confbridge_general'

    @menu_item(
        '.ipbx.advanced.confbridge_general_settings',
        l_('ConfBridge General Settings'),
        order=9,
        icon='asterisk',
    )
    def index(self, form=None):
        return super().index(form)

    def _map_resources_to_form(self, resource):
        resource['wazo_default_user']['options'] = self._build_options(resource['wazo_default_user']['options'])
        resource['wazo_default_bridge']['options'] = self._build_options(resource['wazo_default_bridge']['options'])
        form = self.form(data=resource)
        return form

    def _map_form_to_resources(self, form, form_id=None):
        data = form.to_dict()
        data['wazo_default_user']['options'] = self._map_options_to_resource(data['wazo_default_user']['options'])
        data['wazo_default_bridge']['options'] = self._map_options_to_resource(data['wazo_default_bridge']['options'])
        return data


class PJSIPDocListingView(LoginRequiredView):

    def list_json_by_section(self, section):
        params = extract_select2_params(request.args)
        doc = list(self.service.get().get(section, {}).keys())
        with_id = [{'id': key, 'text': key} for key in doc]
        return jsonify(build_select2_response(with_id, len(doc), params))
