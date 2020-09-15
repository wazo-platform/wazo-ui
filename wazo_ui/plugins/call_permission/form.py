# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    SubmitField,
    StringField,
    SelectMultipleField,
    HiddenField,
    FieldList,
    FormField
)
from wtforms.validators import InputRequired

from wazo_ui.helpers.form import BaseForm, SelectField

mode_map = {
    'allow': l_('Allow'),
    'deny': l_('Deny')
}


class ExtensionsForm(BaseForm):
    exten = StringField()


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class GroupForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class OutcallForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class CallPermissionForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    password = StringField(l_('Password'))
    extensions = FieldList(FormField(ExtensionsForm))
    mode = SelectField(l_('Mode'), choices=[(k, v) for k, v in mode_map.items()])
    user_uuids = SelectMultipleField(l_('Users'), choices=[])
    users = FieldList(FormField(UserForm))
    group_ids = SelectMultipleField(l_('Groups'), choices=[])
    groups = FieldList(FormField(GroupForm))
    outcall_ids = SelectMultipleField(l_('Outcalls'), choices=[])
    outcalls = FieldList(FormField(OutcallForm))
    description = StringField(l_('Description'))
    enabled = BooleanField(l_('Enabled'))
    submit = SubmitField(l_('Submit'))
