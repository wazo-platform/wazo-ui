# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wtforms.fields import (
    FormField,
    BooleanField,
    SelectField,
    HiddenField,
    FieldList,
    SubmitField
)
from wtforms.validators import InputRequired

from wazo_ui.helpers.form import BaseForm


class ServicesForm(BaseForm):
    uuid = SelectField(choices=[], validators=[InputRequired()])
    favorites = BooleanField()
    reverse = BooleanField()
    lookup = BooleanField()


class DirdProfileForm(BaseForm):
    uuid = HiddenField()
    services = FieldList(FormField(ServicesForm))
    submit = SubmitField()
