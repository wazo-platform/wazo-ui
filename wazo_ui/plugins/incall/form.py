# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.destination import DestinationField
from wazo_ui.helpers.form import BaseForm


class ExtensionForm(BaseForm):
    id = HiddenField()
    exten = SelectField(l_('Did'), [InputRequired()], choices=[])
    context = SelectField(l_('Context'), choices=[])


class ScheduleForm(BaseForm):
    id = SelectField(l_('Schedule'), choices=[])
    name = HiddenField()


class IncallForm(BaseForm):
    extensions = FieldList(FormField(ExtensionForm), min_entries=1)
    destination = DestinationField()
    preprocess_subroutine = StringField(l_('Preprocess Subroutine'), [Length(max=79)])
    greeting_sound = SelectField(
        l_('Greeting sound'), choices=[], validators=[Length(max=255)]
    )
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
    schedules = FieldList(FormField(ScheduleForm), min_entries=1)
    submit = SubmitField(l_('Submit'))
