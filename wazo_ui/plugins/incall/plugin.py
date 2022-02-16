# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import IncallService
from .view import IncallView

incall = create_blueprint('incall', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        IncallView.service = IncallService(clients['wazo_confd'])
        IncallView.register(incall, route_base='/incalls')
        register_flaskview(incall, IncallView)

        core.register_blueprint(incall)
