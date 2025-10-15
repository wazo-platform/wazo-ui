# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint

from ..dird_source.service import DirdSourceService
from .service import DirdProfileService
from .view import DirdProfileView

dird_profile = create_blueprint('dird_profile', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        DirdProfileView.service = DirdProfileService(clients['wazo_dird'])
        DirdProfileView.source_service = DirdSourceService(clients['wazo_dird'])
        DirdProfileView.register(dird_profile, route_base='/dird_profiles')
        register_flaskview(dird_profile, DirdProfileView)

        core.register_blueprint(dird_profile)
