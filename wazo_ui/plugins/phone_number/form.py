# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import BooleanField, HiddenField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp

from wazo_ui.helpers.form import BaseForm


class PhoneNumberForm(BaseForm):
    number = StringField(
        l_('Number'), [InputRequired(), Length(min=1, max=128), Regexp(r'^\+?[0-9]+$')]
    )
    caller_id_name = StringField(l_('Caller ID name'), [Length(min=1, max=256)])
    shared = BooleanField(l_('Shared'), default=False)
    main = BooleanField(l_('Main'))
    hidden_main = HiddenField()
    submit = SubmitField(l_('Submit'))
