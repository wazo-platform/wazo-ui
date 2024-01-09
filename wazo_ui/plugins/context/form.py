# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    SubmitField,
    StringField,
    IntegerField,
    SelectField,
    SelectMultipleField,
    FormField,
    FieldList,
    HiddenField,
)
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm


class _ContextForm(BaseForm):
    id = HiddenField()
    label = HiddenField()


class BaseRangesForm(BaseForm):
    start = StringField(l_('Start'), validators=[InputRequired(), Length(max=16)])
    end = StringField(l_('End'), validators=[Length(max=16)])


class IncallRangesForm(BaseRangesForm):
    did_length = IntegerField(l_('DID length'), validators=[InputRequired()])


class ContextForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=79)])
    label = StringField(l_('Label'), validators=[InputRequired(), Length(max=128)])
    type = SelectField(
        l_('Type'),
        choices=[
            ('internal', l_('Internal')),
            ('incall', l_('Incall')),
            ('outcall', l_('Outcall')),
            ('services', l_('Services')),
            ('others', l_('Others')),
        ],
        validators=[InputRequired()],
    )
    description = StringField(l_('Description'))
    user_ranges = FieldList(FormField(BaseRangesForm))
    queue_ranges = FieldList(FormField(BaseRangesForm))
    group_ranges = FieldList(FormField(BaseRangesForm))
    conference_room_ranges = FieldList(FormField(BaseRangesForm))
    incall_ranges = FieldList(FormField(IncallRangesForm))
    context_ids = SelectMultipleField(l_('Contexts included'), choices=[], default=[])
    contexts = FieldList(FormField(_ContextForm))
    submit = SubmitField(l_('Submit'))
