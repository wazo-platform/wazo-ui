# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_ui.helpers.destination import register_destination_form
from wazo_ui.helpers.funckey import register_funckey_destination_form
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import QueueService
from .view import QueueView, QueueDestinationView
from .form import QueueDestinationForm, QueueFuncKeyDestinationForm

queue = create_blueprint('queue', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        QueueView.service = QueueService(clients['wazo_confd'])
        QueueView.register(queue, route_base='/queues')
        register_flaskview(queue, QueueView)

        QueueDestinationView.service = QueueService(clients['wazo_confd'])
        QueueDestinationView.register(queue, route_base='/queue_destination')

        register_destination_form('queue', 'Queue', QueueDestinationForm)
        register_funckey_destination_form('queue', l_('Queue'), QueueFuncKeyDestinationForm)
        register_listing_url('queue', 'queue.QueueDestinationView:list_json')

        core.register_blueprint(queue)
