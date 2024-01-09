# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.view import BaseIPBXHelperView
from wazo_ui.helpers.menu import menu_item

from .form import PagingForm


class PagingView(BaseIPBXHelperView):
    form = PagingForm
    resource = 'paging'

    @menu_item(
        '.ipbx.services.pagings', l_('Pagings'), icon="bullhorn", multi_tenant=True
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        members = [user['uuid'] for user in resource['members']['users']]
        callers = [user['uuid'] for user in resource['callers']['users']]
        resource['members']['user_uuids'] = members
        resource['callers']['user_uuids'] = callers
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.members.user_uuids.choices = self._build_set_choices_users(
            form.members.users
        )
        form.callers.user_uuids.choices = self._build_set_choices_users(
            form.callers.users
        )
        return form

    def _build_set_choices_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = f'{user.firstname.data} {user.lastname.data}'
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['members']['users'] = [
            {'uuid': user_uuid} for user_uuid in form.members.user_uuids.data
        ]
        resource['callers']['users'] = [
            {'uuid': user_uuid} for user_uuid in form.callers.user_uuids.data
        ]
        return resource

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('paging', {}))
        return form
