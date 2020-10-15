# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    SubmitField,
    StringField,
)
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm


class PhonebookForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=80)])
    submit = SubmitField(l_('Submit'))
