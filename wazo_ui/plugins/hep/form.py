# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.widgets import PasswordInput

from wazo_ui.helpers.form import BaseForm


class HepForm(BaseForm):
    enabled = BooleanField(l_('Enabled'))
    capture_address = StringField(l_('Capture Address'))
    capture_password = StringField(
        l_('Capture Password'), widget=PasswordInput(hide_value=False)
    )
    capture_id = StringField(l_('Capture ID'))
    uuid_type = SelectField(
        l_('UUID Type'),
        choices=[('call-id', l_('Call ID')), ('channel', l_('Channel'))],
    )
    submit = SubmitField(l_('Submit'))
