# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_ui.helpers.destination import register_destination_form
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import VoicemailService
from .view import VoicemailView, VoicemailDestinationView
from .form import VoicemailDestinationForm

voicemail = create_blueprint('voicemail', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        VoicemailView.service = VoicemailService(clients['wazo_confd'])
        VoicemailView.register(voicemail, route_base='/voicemails')
        register_flaskview(voicemail, VoicemailView)

        VoicemailDestinationView.service = VoicemailService(clients['wazo_confd'])
        VoicemailDestinationView.register(voicemail, route_base='/voicemails_listing')

        register_destination_form('voicemail', l_('Voicemail'), VoicemailDestinationForm)

        register_listing_url('voicemail', 'voicemail.VoicemailDestinationView:list_json')

        core.register_blueprint(voicemail)
