# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    SubmitField,
    FieldList,
    FormField,
    HiddenField,
    StringField,
    SelectField,
    SelectMultipleField,
    BooleanField,
    FloatField,
)
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.destination import (
    DestinationField,
    DestinationHiddenField,
    FallbacksForm,
)


class OptionsForm(BaseForm):
    option_key = StringField(validators=[InputRequired()])
    option_value = StringField(validators=[InputRequired()])


class ExtensionForm(BaseForm):
    exten = SelectField(choices=[])
    context = SelectField(l_('Context'), choices=[])


class ScheduleForm(BaseForm):
    id = SelectField(l_('Schedule'), choices=[])
    name = HiddenField()


class CallPermissionForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class AgentForm(BaseForm):
    id = HiddenField()
    number = HiddenField()


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class MembersForm(BaseForm):
    agent_ids = SelectMultipleField(l_('Agents'), choices=[], default=[])
    agents = FieldList(FormField(AgentForm))
    user_ids = SelectMultipleField(l_('Users'), choices=[], default=[])
    users = FieldList(FormField(UserForm))


class QueueForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=128)])
    label = StringField(l_('Label'), [InputRequired(), Length(max=128)])

    announce_hold_time_on_entry = BooleanField(
        l_('Announce hold time on entry'), default=False
    )
    music_on_hold = SelectField(l_('Music On Hold'), [Length(max=128)], choices=[])
    data_quality = BooleanField(l_('Data quality'), default=False)
    caller_id_mode = SelectField(
        l_('Caller ID mode'),
        choices=[
            ('', l_('None')),
            ('prepend', l_('Prepend')),
            ('overwrite', l_('Overwrite')),
            ('append', l_('Append')),
        ],
    )
    caller_id_name = StringField(l_('Caller ID name'), [Length(max=80)])

    dtmf_hangup_callee_enabled = BooleanField(
        l_('DTMF hangup callee enabled'), default=False
    )
    dtmf_hangup_caller_enabled = BooleanField(
        l_('DTMF hangup caller enabled'), default=False
    )
    dtmf_record_callee_enabled = BooleanField(
        l_('DTMF record callee enabled'), default=False
    )
    dtmf_record_caller_enabled = BooleanField(
        l_('DTMF record caller enabled'), default=False
    )
    dtmf_transfer_callee_enabled = BooleanField(
        l_('DTMF transfer callee enabled'), default=False
    )
    dtmf_transfer_caller_enabled = BooleanField(
        l_('DTMF transfer caller enabled'), default=False
    )

    ignore_forward = BooleanField(l_('Ignore forward'), default=False)
    preprocess_subroutine = StringField(l_('Subroutine'), [Length(max=39)])
    retry_on_timeout = BooleanField(l_('Retry on timeout'), default=False)
    ring_on_hold = BooleanField(l_('Ring on hold'), default=False)
    timeout = IntegerField(l_('Timeout'), [NumberRange(min=0)])

    wait_ratio_destination = DestinationField(
        destination_label=l_('Wait ratio destination')
    )
    wait_ratio_threshold = FloatField(l_('Wait ratio threshold'), [NumberRange(min=0)])
    wait_time_destination = DestinationField(
        destination_label=l_('Wait time destination')
    )
    wait_time_threshold = IntegerField(l_('Wait time threshold'), [NumberRange(min=0)])

    extensions = FieldList(FormField(ExtensionForm), min_entries=1)
    fallbacks = FormField(FallbacksForm)
    schedules = FieldList(FormField(ScheduleForm), min_entries=1)
    options = FieldList(FormField(OptionsForm))

    enabled = BooleanField(l_('Enabled'), default=False)
    members = FormField(MembersForm)
    mark_answered_elsewhere = BooleanField(
        l_('Mark all calls as answered elsewhere when cancelled'), default=False
    )

    submit = SubmitField(l_('Submit'))


class QueueDestinationForm(BaseForm):
    set_value_template = '{queue_label}'

    queue_id = SelectField(l_('Queue'), [InputRequired()], choices=[])
    ring_time = IntegerField(l_('Ring Time'), [NumberRange(min=0)])
    queue_label = DestinationHiddenField()
    skill_rule_id = SelectField(l_('Skill Rule'), description='skillrule', choices=[])
    skill_rule_variables = StringField(l_('Skill Rule Variables'))


class QueueFuncKeyDestinationForm(BaseForm):
    set_value_template = '{queue_name}'

    queue_id = SelectField(l_('Queue'), [InputRequired()], choices=[])
    queue_name = DestinationHiddenField()
