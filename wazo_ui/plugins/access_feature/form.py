# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    SubmitField,
    StringField,
    SelectField,
)

from wtforms.validators import InputRequired

from nestbox_ui.helpers.form import BaseForm


class AccessFeatureForm(BaseForm):
    feature = SelectField(l_('Feature'),
                       choices=[('phonebook', l_('Phonebook'))],
                       validators=[InputRequired()])
    host = StringField(l_('Host'))
    submit = SubmitField(l_('Submit'))
