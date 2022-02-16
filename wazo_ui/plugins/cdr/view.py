# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView, IndexAjaxHelperViewMixin


class CdrView(IndexAjaxHelperViewMixin, BaseIPBXHelperView):
    form = object
    resource = 'cdr'

    @menu_item('.ipbx.reporting', l_('Reporting'), icon="pie-chart")
    @menu_item('.ipbx.reporting.cdrs', l_('CDR'), icon="newspaper-o")
    def index(self):
        return super().index()
