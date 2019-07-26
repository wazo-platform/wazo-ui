# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import HepService
from .view import HepView


hep = create_blueprint('hep', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        HepView.service = HepService(clients['wazo_confd'])
        HepView.register(hep, route_base='/hep')
        register_flaskview(hep, HepView)

        core.register_blueprint(hep)
