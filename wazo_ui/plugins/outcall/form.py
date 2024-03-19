# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

from wazo_ui.helpers.form import BaseForm


class ScheduleForm(BaseForm):
    id = SelectField(l_('Schedule'), choices=[])
    name = HiddenField()


class CallPermissionForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class OutcallExtensionForm(BaseForm):
    id = HiddenField()
    context = SelectField(l_('Context'), [InputRequired()], choices=[])
    exten = StringField(l_('Extension'), [InputRequired(), Length(max=40)])
    caller_id = StringField(l_('Caller ID'), [Length(max=80)])
    external_prefix = StringField(l_('External prefix'), [Length(max=64)])
    prefix_ = StringField(l_('Prefix'), [Length(max=64)])
    strip_digits = IntegerField(l_('Strip digits'), [NumberRange(min=0)], default=0)


class TrunkForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class OutcallForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=128)])
    description = StringField(l_('Description'))
    extensions = FieldList(FormField(OutcallExtensionForm))
    trunks_ids = SelectMultipleField(l_('Trunks'), choices=[])
    trunks = FieldList(FormField(TrunkForm))
    preprocess_subroutine = StringField(l_('Preprocess Subroutine'))
    internal_caller_id = BooleanField(l_('Internal Caller ID'), default=False)
    ring_time = IntegerField(l_('Ring time'), [NumberRange(min=0)])
    schedules = FieldList(FormField(ScheduleForm), min_entries=1)
    call_permission_ids = SelectMultipleField(l_('Call Permissions'), choices=[])
    call_permissions = FieldList(FormField(CallPermissionForm))
    submit = SubmitField(l_('Submit'))
