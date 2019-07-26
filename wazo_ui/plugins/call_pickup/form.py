# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    SubmitField,
    StringField,
    HiddenField,
    SelectMultipleField,
    FieldList,
    FormField
)
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class GroupForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class InterceptorsForm(BaseForm):
    user_uuids = SelectMultipleField(l_('Interceptor Users'), choices=[], default=[])
    users = FieldList(FormField(UserForm))
    group_ids = SelectMultipleField(l_('Interceptor Groups'), choices=[], default=[])
    groups = FieldList(FormField(GroupForm))


class TargetsForm(BaseForm):
    user_uuids = SelectMultipleField(l_('Target Users'), choices=[], default=[])
    users = FieldList(FormField(UserForm))
    group_ids = SelectMultipleField(l_('Target Groups'), choices=[], default=[])
    groups = FieldList(FormField(GroupForm))


class CallPickupForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=128)])
    interceptors = FormField(InterceptorsForm)
    targets = FormField(TargetsForm)
    description = StringField(l_('Description'))
    enabled = BooleanField(l_('Enabled'))
    submit = SubmitField(l_('Submit'))
