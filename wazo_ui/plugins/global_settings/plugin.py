# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .view import GlobalSettingsView

global_settings = create_blueprint('global_settings', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']

        GlobalSettingsView.register(global_settings, route_base='/global_settings')
        register_flaskview(global_settings, GlobalSettingsView)

        core.register_blueprint(global_settings)
