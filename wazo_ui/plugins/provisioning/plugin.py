# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import PluginService, ConfigService, ConfigurationService
from .view import PluginView, PluginListingView, ConfigRegistrarView, ConfigDeviceView, ConfigurationView, ConfigDeviceListingView

provisioning = create_blueprint('provisioning', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PluginView.service = PluginService(clients['wazo_provd'])
        PluginView.register(provisioning, route_base='/provisioning/plugins')
        register_flaskview(provisioning, PluginView)

        ConfigRegistrarView.service = ConfigService(clients['wazo_provd'])
        ConfigRegistrarView.register(provisioning, route_base='/provisioning/configs/registrar')
        register_flaskview(provisioning, ConfigRegistrarView)

        ConfigDeviceView.service = ConfigService(clients['wazo_provd'])
        ConfigDeviceView.register(provisioning, route_base='/provisioning/configs/device')
        register_flaskview(provisioning, ConfigDeviceView)

        ConfigDeviceListingView.service = ConfigService(clients['wazo_provd'])
        ConfigDeviceListingView.register(provisioning, route_base='/config_devices_listing')
        register_flaskview(provisioning, ConfigDeviceListingView)

        PluginListingView.service = PluginService(clients['wazo_provd'])
        PluginListingView.register(provisioning, route_base='/plugins_listing')

        register_listing_url('plugin', 'provisioning.PluginListingView:list_json')
        register_listing_url('config_device', 'provisioning.ConfigDeviceListingView:list_json')

        ConfigurationView.service = ConfigurationService(clients['wazo_provd'], clients['wazo_confd'])
        ConfigurationView.register(provisioning, route_base='/provisioning/configuration')
        register_flaskview(provisioning, ConfigurationView)

        core.register_blueprint(provisioning)
