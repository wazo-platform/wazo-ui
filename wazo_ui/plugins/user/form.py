# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FormField,
    FieldList,
    FileField,
    HiddenField,
    SelectField,
    SelectMultipleField,
    SubmitField,
    StringField,
)
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.destination import FallbacksForm, DestinationHiddenField
from wazo_ui.helpers.funckey import FuncKeyDestinationField


class TemplateForm(BaseForm):
    uuid = HiddenField()


class ApplicationForm(BaseForm):
    uuid = SelectField(choices=[])
    name = HiddenField()


class ExtensionForm(BaseForm):
    id = HiddenField()
    exten = SelectField(label='Exten', choices=[])


class ImportCSVForm(BaseForm):
    file = FileField('CSV File')
    submit = SubmitField()


class LineForm(BaseForm):
    id = HiddenField()
    template_uuids = SelectMultipleField(label='Templates', choices=[])
    templates = FieldList(FormField(TemplateForm))
    context = SelectField(label='Context', choices=[])
    endpoint_sip_uuid = HiddenField()
    endpoint_sccp_id = HiddenField()
    endpoint_custom_id = HiddenField()
    protocol = SelectField(
        choices=[
            ('sip', l_('SIP')),
            ('sccp', l_('SCCP')),
            (
                'custom',
                l_('CUSTOM'),
            ),
        ]
    )
    extensions = FieldList(FormField(ExtensionForm), min_entries=1)
    application = FormField(ApplicationForm)
    registrar = SelectField(choices=[])
    name = StringField()
    device = SelectField(choices=[])
    position = IntegerField(default=1, validators=[NumberRange(min=1), InputRequired()])


class BusyForwardForm(BaseForm):
    enabled = BooleanField(l_('Busy'), default=False)
    destination = StringField(l_('Destination'), [Length(max=128)])


class NoAnswerForwardForm(BaseForm):
    enabled = BooleanField(l_('No answer'), default=False)
    destination = StringField(l_('Destination'), [Length(max=128)])


class UnconditionalForwardForm(BaseForm):
    enabled = BooleanField(l_('Unconditional'), default=False)
    destination = StringField(l_('Destination'), [Length(max=128)])


class UserForwardForm(BaseForm):
    busy = FormField(BusyForwardForm)
    noanswer = FormField(NoAnswerForwardForm)
    unconditional = FormField(UnconditionalForwardForm)


class DNDServiceForm(BaseForm):
    enabled = BooleanField(l_('Do not disturb'), default=False)


class IncallFilterServiceForm(BaseForm):
    enabled = BooleanField(l_('Incall filtering'), default=False)


class UserServiceForm(BaseForm):
    dnd = FormField(DNDServiceForm)
    incallfilter = FormField(IncallFilterServiceForm)


class GroupForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class FuncKeyTemplateKeysForm(BaseForm):
    id = HiddenField()
    label = StringField(l_('Label'), [Length(max=128)])
    digit = IntegerField(validators=[InputRequired()])
    destination = FuncKeyDestinationField()
    blf = BooleanField(l_('BLF'), default=False)
    submit = SubmitField()


class ScheduleForm(BaseForm):
    id = SelectField(l_('Schedule'), choices=[])
    name = HiddenField()


class VoicemailForm(BaseForm):
    id = SelectField(l_('Voicemail'), choices=[])
    name = HiddenField()


class CallPermissionForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class UserForm(BaseForm):
    subscription_type = SelectField(
        l_('Subscription Type'),
        choices=[
            (0, l_('Voice')),
            (1, l_('Unified Communication')),
            (2, l_('Collaboration')),
            (3, l_('Customer Relationship')),
        ],
        validators=[InputRequired()],
    )
    firstname = StringField(l_('Firstname'), [InputRequired(), Length(max=128)])
    lastname = StringField(l_('Lastname'), [Length(max=128)])
    username = StringField(l_('Username'), [InputRequired(), Length(min=2, max=254)])
    password = StringField(l_('Password'), [Length(min=4, max=64)])
    email = EmailField(l_('Email'), [InputRequired(), Length(max=254)])
    auth_enabled = BooleanField(l_('Enable authentication'))
    caller_id = StringField(l_('Caller ID'), [Length(max=80)])
    mobile_phone_number = StringField(l_('Phone mobile'), [Length(max=80)])
    ring_seconds = IntegerField(l_('Ring seconds'), [NumberRange(min=0, max=60)])
    music_on_hold = SelectField(l_('Music On Hold'), choices=[])
    preprocess_subroutine = StringField(l_('Subroutine'), [Length(max=79)])
    outgoing_caller_id = SelectField(l_('Outgoing caller ID'))
    simultaneous_calls = IntegerField(
        l_('Simultaneous calls'), [NumberRange(min=1, max=20)]
    )
    timezone = StringField(l_('Timezone'), [Length(max=254)])
    userfield = StringField(l_('User Field'), [Length(max=128)])
    description = StringField(l_('Description'))
    call_permission_password = StringField(l_('Call Permission Password'))
    call_record_outgoing_external_enabled = BooleanField(
        l_('Outgoing external call recording'), default=False
    )
    call_record_outgoing_internal_enabled = BooleanField(
        l_('Outgoing internal call recording'), default=False
    )
    call_record_incoming_external_enabled = BooleanField(
        l_('Incoming external call recording'), default=False
    )
    call_record_incoming_internal_enabled = BooleanField(
        l_('Incoming internal call recording'), default=False
    )
    call_transfer_enabled = BooleanField(l_('Enable Transfer by DTMF'), default=False)
    dtmf_hangup_enabled = BooleanField(l_('Enable Hangup by DTMF'), default=False)
    online_call_record_enabled = BooleanField(
        l_('Enable Live Recording'), default=False
    )
    fallbacks = FormField(FallbacksForm)
    forwards = FormField(UserForwardForm)
    services = FormField(UserServiceForm)
    lines = FieldList(FormField(LineForm))
    group_ids = SelectMultipleField(l_('Groups'), choices=[])
    groups = FieldList(FormField(GroupForm))
    funckeys = FieldList(FormField(FuncKeyTemplateKeysForm))
    schedules = FieldList(FormField(ScheduleForm), min_entries=1)
    voicemail = FormField(VoicemailForm)
    call_permission_ids = SelectMultipleField(l_('Call Permissions'), choices=[])
    call_permissions = FieldList(FormField(CallPermissionForm))
    submit = SubmitField(l_('Submit'))


class UserDestinationForm(BaseForm):
    set_value_template = '{user_firstname} {user_lastname}'

    user_id = SelectField(l_('User'), choices=[], validators=[InputRequired()])
    ring_time = IntegerField(l_('Ring time'), [NumberRange(min=0)])
    user_firstname = DestinationHiddenField()
    user_lastname = DestinationHiddenField()


class UserFuncKeyDestinationForm(BaseForm):
    set_value_template = '{user_firstname} {user_lastname}'

    user_id = SelectField(l_('User'), [InputRequired()], choices=[])
    user_firstname = DestinationHiddenField()
    user_lastname = DestinationHiddenField()
