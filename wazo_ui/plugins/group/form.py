# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    SubmitField,
    FieldList,
    FormField,
    HiddenField,
    StringField,
    SelectField,
    SelectMultipleField,
    BooleanField
)
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.destination import FallbacksForm, DestinationHiddenField


class ExtensionForm(BaseForm):
    exten = SelectField(choices=[])
    context = SelectField(l_('Context'), choices=[])


class ExtensionsMembersForm(BaseForm):
    exten = StringField(l_('Extension'), [InputRequired(), Length(max=128)])
    context = StringField(l_('Context'), [InputRequired(), Length(max=128)])
    priority = HiddenField(default=1)


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class MembersForm(BaseForm):
    user_uuids = SelectMultipleField(l_('Members'), choices=[])
    users = FieldList(FormField(UserForm))


class ScheduleForm(BaseForm):
    id = SelectField(l_('Schedule'), choices=[])
    name = HiddenField()


class CallPermissionForm(BaseForm):
    id = HiddenField()
    name = HiddenField()


class GroupForm(BaseForm):
    name = StringField(l_('Name'), render_kw={'disabled': True})
    label = StringField(l_('Label'), [InputRequired(), Length(max=128)])
    extensions = FieldList(FormField(ExtensionForm), min_entries=1)
    caller_id_mode = SelectField(l_('Callerid mode'), choices=[
        ('', l_('None')),
        ('prepend', l_('Prepend')),
        ('overwrite', l_('Overwrite')),
        ('append', l_('Append'))
    ])
    caller_id_name = StringField('Callerid name', [Length(max=80)])
    enabled = BooleanField(l_('Enabled'))
    music_on_hold = SelectField('Music On Hold', [Length(max=128)], choices=[])
    preprocess_subroutine = StringField(l_('Subroutine'), [Length(max=39)])
    retry_delay = IntegerField('Retry delay', [NumberRange(min=0)])
    ring_in_use = BooleanField('Ring in use', default=False)
    ring_strategy = SelectField('Ring strategy', choices=[
        ('all', l_('All')),
        ('random', l_('Random')),
        ('least_recent', l_('Least recent')),
        ('linear', l_('Linear')),
        ('fewest_calls', l_('Fewest calls')),
        ('memorized_round_robin', l_('Memorized round robin'))
    ])
    timeout = IntegerField(l_('Timeout'), [NumberRange(min=0)])
    user_timeout = IntegerField(l_('User timeout'), [NumberRange(min=0)])
    members = FormField(MembersForm)
    extensions_members = FieldList(FormField(ExtensionsMembersForm))
    fallbacks = FormField(FallbacksForm)
    schedules = FieldList(FormField(ScheduleForm), min_entries=1)
    call_permission_ids = SelectMultipleField(l_('Call Permissions'), choices=[])
    call_permissions = FieldList(FormField(CallPermissionForm))
    mark_answered_elsewhere = BooleanField(l_('Mark all calls as answered elsewhere when cancelled'), default=False)
    submit = SubmitField(l_('Submit'))


class GroupDestinationForm(BaseForm):
    set_value_template = '{group_name}'

    group_id = SelectField(l_('Group'), [InputRequired()], choices=[])
    ring_time = IntegerField(l_('Ring Time'), [NumberRange(min=0)])
    group_name = DestinationHiddenField()


class GroupFuncKeyDestinationForm(BaseForm):
    set_value_template = '{group_name}'

    group_id = SelectField(l_('Group'), [InputRequired()], choices=[])
    group_name = DestinationHiddenField()


class GroupMemberFuncKeyDestinationForm(BaseForm):
    set_value_template = '{group_name}'

    action = SelectField(l_('Action'), [InputRequired()],
                         choices=[('join', l_('Join group')),
                                  ('leave', l_('Leave group')),
                                  ('toggle', l_('Join or leave group'))],
                         default='toggle')
    group_id = SelectField(l_('Group'), [InputRequired()], choices=[])
    group_name = DestinationHiddenField()
