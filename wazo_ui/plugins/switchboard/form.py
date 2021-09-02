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
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.destination import FallbacksForm, DestinationHiddenField


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
    queue_music_on_hold = SelectField(l_('Music On Hold'), [Length(max=128)], choices=[])
    waiting_room_music_on_hold = SelectField(l_('Waiting Room Music On Hold'), [Length(max=128)], choices=[])
    fallbacks = FormField(FallbacksForm)
    timeout = IntegerField(l_('Timeout'), [NumberRange(min=1)])
    submit = SubmitField(l_('Submit'))


class SwitchboardDestinationForm(BaseForm):
    set_value_template = '{switchboard_name}'

    switchboard_uuid = SelectField(l_('Switchboard'), [InputRequired()], choices=[])
    switchboard_name = DestinationHiddenField()
