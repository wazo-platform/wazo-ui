# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .service import RecordingAnnouncementService
from .view import RecordingAnnouncementView

recording_announcement = create_blueprint('recording_announcement', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        RecordingAnnouncementView.service = RecordingAnnouncementService(
            clients['wazo_confd']
        )
        RecordingAnnouncementView.register(
            recording_announcement, route_base='/recording_announcement'
        )
        register_flaskview(recording_announcement, RecordingAnnouncementView)

        core.register_blueprint(recording_announcement)
