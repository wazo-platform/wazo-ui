# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_ui.helpers.destination import register_destination_form
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .form import SoundDestinationForm
from .service import SoundService
from .view import SoundView, SoundListingView, SoundFileView

sound = create_blueprint('sound', __name__)


class Plugin(object):
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        SoundView.service = SoundService(clients['wazo_confd'])
        SoundView.register(sound, route_base='/sound')
        register_flaskview(sound, SoundView)

        SoundFileView.service = SoundService(clients['wazo_confd'])
        SoundFileView.register(sound, route_base='/sound_files')
        register_flaskview(sound, SoundFileView)

        SoundListingView.service = SoundService(clients['wazo_confd'])
        SoundListingView.register(sound, route_base='/sound_listing')

        register_destination_form('sound', l_('Sound'), SoundDestinationForm)

        register_listing_url('sound', 'sound.SoundListingView:list_json')

        core.register_blueprint(sound)
