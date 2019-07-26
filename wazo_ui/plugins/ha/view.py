# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import (
    jsonify,
    render_template,
    request,
    flash
)
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from flask_classful import route
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import LoginRequiredView
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import HaForm


class HaView(BaseIPBXHelperView):
    form = HaForm
    resource = 'ha'

    @menu_item('.ipbx.network.ha', l_('High Availability'), order=2, icon="balance-scale")
    def index(self):
        try:
            resource = self.service.get()
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        return render_template(self._get_template('index'),
                               form=self.form(data=resource))

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

        flash(_('High Availabitity config has been updated'), 'success')
        return self._redirect_for('index')
