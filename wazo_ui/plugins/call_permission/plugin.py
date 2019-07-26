# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import CallPermissionService
from .view import CallPermissionView, CallPermissionListingView

call_permission = create_blueprint('call_permission', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        CallPermissionView.service = CallPermissionService(clients['wazo_confd'])
        CallPermissionView.register(call_permission, route_base='/callpermissions')
        register_flaskview(call_permission, CallPermissionView)

        CallPermissionListingView.service = CallPermissionService(clients['wazo_confd'])
        CallPermissionListingView.register(call_permission, route_base='/callpermissions_listing')

        register_listing_url('callpermission', 'call_permission.CallPermissionListingView:list_json')

        core.register_blueprint(call_permission)
