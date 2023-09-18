# Copyright 2021-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint

from .service import (
    ManagePhonebookContactsService,
    PhonebookService,
)
from .view import PhonebookView, ManagePhonebookView

phonebook = create_blueprint('phonebook', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PhonebookView.service = PhonebookService(clients['wazo_dird'])
        PhonebookView.register(phonebook, route_base='/phonebooks')
        register_flaskview(phonebook, PhonebookView)

        ManagePhonebookView.service = ManagePhonebookContactsService(
            clients['wazo_dird']
        )
        ManagePhonebookView.register(phonebook, route_base='/manage_phonebooks')
        register_flaskview(phonebook, ManagePhonebookView)

        core.register_blueprint(phonebook)
