# Copyright 2017-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import ScheduleService
from .view import ScheduleListingView, ScheduleView

schedule = create_blueprint('schedule', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ScheduleView.service = ScheduleService(clients['wazo_confd'])
        ScheduleView.register(schedule, route_base='/schedules')
        register_flaskview(schedule, ScheduleView)

        ScheduleListingView.service = ScheduleService(clients['wazo_confd'])
        ScheduleListingView.register(schedule, route_base='/schedules_listing')

        register_listing_url('schedule', 'schedule.ScheduleListingView:list_json')

        core.register_blueprint(schedule)
