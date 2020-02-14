# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import (
    PJSIPGlobalSettingsService,
    SipGeneralSettingsService,
    IaxGeneralSettingsService,
    SccpGeneralSettingsService,
    VoicemailGeneralSettingsService,
    FeaturesGeneralSettingsService,
    ConfBridgeGeneralSettingsService
)
from .view import (
    PJSIPGlobalSettingsView,
    SipGeneralSettingsView,
    IaxGeneralSettingsView,
    SccpGeneralSettingsView,
    VoicemailGeneralSettingsView,
    FeaturesGeneralSettingsView,
    ConfBridgeGeneralSettingsView
)

general_settings = create_blueprint('general_settings', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PJSIPGlobalSettingsView.service = PJSIPGlobalSettingsService(clients['wazo_confd'])
        PJSIPGlobalSettingsView.register(general_settings, route_base='/pjsip_global_settings')
        register_flaskview(general_settings, PJSIPGlobalSettingsView)

        SipGeneralSettingsView.service = SipGeneralSettingsService(clients['wazo_confd'])
        SipGeneralSettingsView.register(general_settings, route_base='/sip_general_settings')
        register_flaskview(general_settings, SipGeneralSettingsView)

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

        core.register_blueprint(general_settings)
