# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import ParkingLotService
from .view import ParkingLotView

parking_lot = create_blueprint('parking_lot', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ParkingLotView.service = ParkingLotService(clients['wazo_confd'])
        ParkingLotView.register(parking_lot, route_base='/parkinglots')
        register_flaskview(parking_lot, ParkingLotView)

        core.register_blueprint(parking_lot)
