# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint

from .service import PhonebookService
from .view import PhonebookView

phonebook = create_blueprint('phonebook', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PhonebookView.service = PhonebookService(clients['wazo_dird'])
        PhonebookView.register(phonebook, route_base='/phonebooks')
        register_flaskview(phonebook, PhonebookView)

        core.register_blueprint(phonebook)
