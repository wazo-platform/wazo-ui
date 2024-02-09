# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_ui.helpers.funckey import register_funckey_destination_form
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .form import ParkingFuncKeyDestinationForm
from .service import ParkingLotService
from .view import ParkingLotDestinationView, ParkingLotView

parking_lot = create_blueprint('parking_lot', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ParkingLotView.service = ParkingLotService(clients['wazo_confd'])
        ParkingLotView.register(parking_lot, route_base='/parkinglots')
        register_flaskview(parking_lot, ParkingLotView)

        ParkingLotDestinationView.service = ParkingLotService(clients['wazo_confd'])
        ParkingLotDestinationView.register(
            parking_lot, route_base='/parking_lot_destination'
        )

        register_funckey_destination_form(
            'parking', l_('Parking'), ParkingFuncKeyDestinationForm
        )
        register_listing_url(
            'parking', 'parking_lot.ParkingLotDestinationView:list_json'
        )

        core.register_blueprint(parking_lot)
