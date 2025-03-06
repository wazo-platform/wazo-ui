# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import flash, render_template
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import RecordingAnnouncementForm


class RecordingAnnouncementView(BaseIPBXHelperView):
    form = RecordingAnnouncementForm
    resource = 'recording_announcement'

    @menu_item(
        '.ipbx.sound_greeting.recording_announcement',
        l_('Recording Announcement'),
        icon="bullhorn",
        multi_tenant=True,
    )
    def index(self):
        try:
            resource_list = self.service.get()
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        form = self._populate_form(self.form(data=resource_list))

        return render_template(
            self._get_template('index'),
            form=form,
            resource_list=resource_list,
            current_breadcrumbs=self._get_current_breadcrumbs(),
        )

    def post(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._index(form)

        resource = form.to_dict()

        try:
            self.service.update(resource)
        except HTTPError as error:
            self._flash_http_error(error)
            return self.index()

        flash(_('Recording announcement config has been updated'), 'success')
        return self._redirect_for('index')
