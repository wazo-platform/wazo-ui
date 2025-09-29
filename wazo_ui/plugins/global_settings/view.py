# Copyright 2020-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import render_template
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import LoginRequiredView
from wazo_ui.helpers.menu import menu_item


class GlobalSettingsView(LoginRequiredView):
    @menu_item(
        '.ipbx.global_settings',
        l_('Global Settings'),
        order=1000,
        icon="gears",
        multi_tenant=False,
    )
    def index(self):
        return render_template('global_settings/index.html')
