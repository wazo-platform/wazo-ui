# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import CdrService
from .view import CdrView

cdr = create_blueprint('cdr', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        CdrView.service = CdrService(clients['wazo_call_logd'])
        CdrView.register(cdr, route_base='/cdrs')
        register_flaskview(cdr, CdrView)

        core.register_blueprint(cdr)
