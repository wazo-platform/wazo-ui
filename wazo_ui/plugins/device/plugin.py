# Copyright 2017-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import DeviceService
from .view import DeviceListingView, DeviceView

device = create_blueprint('device', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        DeviceView.service = DeviceService(clients['wazo_confd'], clients['wazo_provd'])
        DeviceView.register(device, route_base='/devices')
        register_flaskview(device, DeviceView)

        DeviceListingView.service = DeviceService(
            clients['wazo_confd'], clients['wazo_provd']
        )
        DeviceListingView.register(device, route_base='/devices_listing')

        register_listing_url('device', 'device.DeviceListingView:list_json')

        core.register_blueprint(device)
