# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    HiddenField,
    SubmitField,
    StringField,
    BooleanField,
    SelectMultipleField,
)

from wtforms.validators import InputRequired, Length, Regexp

from wazo_ui.helpers.form import BaseForm


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class MembersForm(BaseForm):
    user_uuids = SelectMultipleField(l_('Members'), choices=[])
    users = FieldList(FormField(UserForm))


class CallersForm(BaseForm):
    user_uuids = SelectMultipleField(l_('Callers'), choices=[])
    users = FieldList(FormField(UserForm))


class PagingForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=128)])
    context = StringField(default='default')
    number = StringField(
        l_('Number'), [InputRequired(), Length(max=32), Regexp(r'^[0-9]+$')]
    )
    members = FormField(MembersForm)
    callers = FormField(CallersForm)
    announce_caller = BooleanField(l_('Announce caller'), default=False)
    announce_sound = StringField(l_('Announce sound'), [Length(max=64)], default='')
    caller_notification = BooleanField(l_('Play notification to caller'), default=False)
    duplex = BooleanField(l_('Duplex audio'), default=False)
    enabled = BooleanField(l_('Enabled'), default=False)
    ignore_forward = BooleanField(l_('Ignore forward'), default=False)
    record = BooleanField(l_('Announce caller'), default=False)
    submit = SubmitField(l_('Submit'))
