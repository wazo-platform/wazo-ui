# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FieldList,
    FormField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length, Regexp

from wazo_ui.helpers.destination import DestinationHiddenField
from wazo_ui.helpers.form import BaseForm


class ExtensionForm(BaseForm):
    exten = SelectField(l_('Extension'), choices=[])
    context = SelectField(l_('Context'), choices=[])


class ConferenceForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=128)])
    extensions = FieldList(FormField(ExtensionForm), min_entries=1)
    announce_join_leave = BooleanField(l_('Announce join leave'), default=False)
    announce_only_user = BooleanField(l_('Announce only user'), default=False)
    announce_user_count = BooleanField(l_('Announce user count'), default=False)
    music_on_hold = SelectField('Music On Hold', [Length(max=128)], choices=[])
    pin = StringField(
        l_('PIN'),
        [Regexp(r'^[0-9]+$'), Length(max=80)],
        render_kw={'type': 'password', 'data_toggle': 'password'},
    )
    admin_pin = StringField(
        l_('Admin PIN'),
        [Regexp(r'^[0-9]+$'), Length(max=80)],
        render_kw={'type': 'password', 'data_toggle': 'password'},
    )
    preprocess_subroutine = StringField(l_('Subroutine'), [Length(max=79)])
    quiet_join_leave = BooleanField(l_('Quiet join/leave'), default=False)
    submit = SubmitField()


class ConferenceDestinationForm(BaseForm):
    set_value_template = '{conference_name}'

    conference_id = SelectField('Conference', choices=[], validators=[InputRequired()])
    conference_name = DestinationHiddenField()


class ConferenceFuncKeyDestinationForm(BaseForm):
    set_value_template = '{conference_name}'

    conference_id = SelectField(l_('Conference'), [InputRequired()], choices=[])
    conference_name = DestinationHiddenField()
