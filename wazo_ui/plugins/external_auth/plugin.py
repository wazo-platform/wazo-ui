# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint

from .service import ExternalAuthService
from .view import ExternalAuthView

external_auth = create_blueprint('external_auth', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ExternalAuthView.service = ExternalAuthService(clients['wazo_auth'])
        ExternalAuthView.register(external_auth, route_base='/external_auths')
        register_flaskview(external_auth, ExternalAuthView)

        core.register_blueprint(external_auth)
