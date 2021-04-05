# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import (
    ConfBridgeGeneralSettingsService,
    FeaturesGeneralSettingsService,
    IaxGeneralSettingsService,
    PJSIPDocService,
    PJSIPGlobalSettingsService,
    PJSIPSystemSettingsService,
    SccpGeneralSettingsService,
    TimezoneService,
    VoicemailGeneralSettingsService,
)
from .view import (
    ConfBridgeGeneralSettingsView,
    FeaturesGeneralSettingsView,
    IaxGeneralSettingsView,
    PJSIPDocListingView,
    PJSIPGlobalSettingsView,
    PJSIPSystemSettingsView,
    SccpGeneralSettingsView,
    TimezoneListingView,
    VoicemailGeneralSettingsView,
)

general_settings = create_blueprint('general_settings', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PJSIPDocListingView.service = PJSIPDocService(clients['wazo_confd'])
        PJSIPDocListingView.register(general_settings, route_base='/list_json_by_section')
        register_listing_url('pjsip_doc', 'general_settings.PJSIPDocListingView:list_json_by_section')

        PJSIPGlobalSettingsView.service = PJSIPGlobalSettingsService(clients['wazo_confd'])
        PJSIPGlobalSettingsView.register(general_settings, route_base='/pjsip_global_settings')
        register_flaskview(general_settings, PJSIPGlobalSettingsView)

        PJSIPSystemSettingsView.service = PJSIPSystemSettingsService(clients['wazo_confd'])
        PJSIPSystemSettingsView.register(general_settings, route_base='/pjsip_system_settings')
        register_flaskview(general_settings, PJSIPSystemSettingsView)

        IaxGeneralSettingsView.service = IaxGeneralSettingsService(clients['wazo_confd'])
        IaxGeneralSettingsView.register(general_settings, route_base='/iax_general_settings')
        register_flaskview(general_settings, IaxGeneralSettingsView)

        SccpGeneralSettingsView.service = SccpGeneralSettingsService(clients['wazo_confd'])
        SccpGeneralSettingsView.register(general_settings, route_base='/sccp_general_settings')
        register_flaskview(general_settings, SccpGeneralSettingsView)

        VoicemailGeneralSettingsView.service = VoicemailGeneralSettingsService(clients['wazo_confd'])
        VoicemailGeneralSettingsView.register(general_settings, route_base='/voicemail_general_settings')
        register_flaskview(general_settings, VoicemailGeneralSettingsView)

        FeaturesGeneralSettingsView.service = FeaturesGeneralSettingsService(clients['wazo_confd'])
        FeaturesGeneralSettingsView.register(general_settings, route_base='/features_general_settings')
        register_flaskview(general_settings, FeaturesGeneralSettingsView)

        ConfBridgeGeneralSettingsView.service = ConfBridgeGeneralSettingsService(clients['wazo_confd'])
        ConfBridgeGeneralSettingsView.register(general_settings, route_base='/confbridge_general_settings')
        register_flaskview(general_settings, ConfBridgeGeneralSettingsView)

        TimezoneListingView.service = TimezoneService(clients['wazo_confd'])
        TimezoneListingView.register(general_settings, route_base='/timezones_listing')
        register_flaskview(general_settings, TimezoneListingView)
        register_listing_url('timezone', 'general_settings.TimezoneListingView:list_json')

        core.register_blueprint(general_settings)
