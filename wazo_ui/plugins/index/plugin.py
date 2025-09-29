# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint

from .view import IndexView, WorkingTenantView

index = create_blueprint('index', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']

        IndexView.register(index, route_base='/')
        register_flaskview(index, IndexView)

        WorkingTenantView.register(index, route_base='/set_working_tenant_uuid')
        register_flaskview(index, WorkingTenantView)

        core.register_blueprint(index)
