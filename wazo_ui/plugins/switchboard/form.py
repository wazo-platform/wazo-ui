# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    HiddenField,
    SubmitField,
    StringField,
    SelectField,
    SelectMultipleField
)
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.destination import DestinationHiddenField


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class MembersForm(BaseForm):
    user_uuids = SelectMultipleField(l_('Members'), choices=[])
    users = FieldList(FormField(UserForm))


class SwitchboardForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=128)])
    members = FormField(MembersForm)
    submit = SubmitField(l_('Submit'))


class SwitchboardDestinationForm(BaseForm):
    set_value_template = '{switchboard_name}'

    switchboard_uuid = SelectField(l_('Switchboard'), [InputRequired()], choices=[])
    switchboard_name = DestinationHiddenField()
