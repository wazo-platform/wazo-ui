# Copyright 2019-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint

from .service import RtpService
from .view import RtpView

rtp = create_blueprint('rtp', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        RtpView.service = RtpService(clients['wazo_confd'])
        RtpView.register(rtp, route_base='/rtp')
        register_flaskview(rtp, RtpView)

        core.register_blueprint(rtp)
