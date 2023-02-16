# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .view import ExternalAuthView
from .service import ExternalAuthService

external_auth = create_blueprint('external_auth', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ExternalAuthView.service = ExternalAuthService(clients['wazo_auth'])
        ExternalAuthView.register(external_auth, route_base='/external_auths')
        register_flaskview(external_auth, ExternalAuthView)

        core.register_blueprint(external_auth)
