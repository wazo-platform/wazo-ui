# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ParkingLotForm


class ParkingLotView(BaseIPBXHelperView):
    form = ParkingLotForm
    resource = 'parking_lot'

    @menu_item(
        '.ipbx.services.parkinglots',
        l_('Parking Lots'),
        icon="automobile",
        multi_tenant=True,
    )
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.music_on_hold.choices = self._build_set_choices_moh(form)
        for form_extension in form.extensions:
            form_extension.context.choices = self._build_set_choices_context(
                form_extension
            )
        return form

    def _build_set_choices_moh(self, form):
        if not form.music_on_hold.data or form.music_on_hold.data == 'None':
            return []
        return [(form.music_on_hold.data, form.music_on_hold.data)]

    def _build_set_choices_context(self, form):
        if not form.context.data or form.context.data == 'None':
            return []
        return [(form.context.data, form.context.data)]

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('parking_lot', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['music_on_hold'] = self._convert_empty_string_to_none(
            form.music_on_hold.data
        )
        return resource
