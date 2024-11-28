# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import PhoneNumberService
from .view import PhoneNumberView

phone_number = create_blueprint('phone_number', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PhoneNumberView.service = PhoneNumberService(clients['wazo_confd'])
        PhoneNumberView.register(phone_number, route_base='/phone_number')
        register_flaskview(phone_number, PhoneNumberView)

        core.register_blueprint(phone_number)
