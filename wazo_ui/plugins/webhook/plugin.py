# Copyright 2017-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.menu import register_flaskview
from wazo_ui.helpers.plugin import create_blueprint

from .service import WebhookService
from .view import WebhookView

webhook = create_blueprint('webhook', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        WebhookView.service = WebhookService(
            clients['wazo_webhookd'], clients['wazo_confd']
        )
        WebhookView.register(webhook, route_base='/webhooks')
        register_flaskview(webhook, WebhookView)

        core.register_blueprint(webhook)
