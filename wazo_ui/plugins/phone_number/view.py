# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import PhoneNumberForm


class PhoneNumberView(BaseIPBXHelperView):
    form = PhoneNumberForm
    resource = 'phone_number'

    @menu_item(
        '.ipbx.call_management.phone_numbers',
        l_('Phone Numbers'),
        icon="long-arrow-right",
        order=2,
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _populate_form(self, form):
        return form

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('phone_number', {}))
        return form
