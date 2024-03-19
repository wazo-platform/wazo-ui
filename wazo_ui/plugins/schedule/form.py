# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired

from wazo_ui.helpers.destination import DestinationField
from wazo_ui.helpers.form import BaseForm

week_days = [
    l_('Monday'),
    l_('Tuesday'),
    l_('Wednesday'),
    l_('Thursday'),
    l_('Friday'),
    l_('Saturday'),
    l_('Sunday'),
]
month_days = range(1, 32)
months = [
    l_('January'),
    l_('February'),
    l_('March'),
    l_('April'),
    l_('May'),
    l_('June'),
    l_('July'),
    l_('August'),
    l_('September'),
    l_('October'),
    l_('November'),
    l_('December'),
]


def convert_list_to_choices(list_):
    result = []
    for index, item in enumerate(list_, start=1):
        result.append((index, item))
    return result


class PeriodForm(BaseForm):
    hours_start = StringField(l_('Hour Start'), validators=[InputRequired()])
    hours_end = StringField(l_('Hour End'), validators=[InputRequired()])
    week_days = SelectMultipleField(
        l_('Weekdays'),
        choices=convert_list_to_choices(week_days),
        validators=[InputRequired()],
    )
    month_days = SelectMultipleField(
        l_('Monthdays'),
        choices=convert_list_to_choices(month_days),
        validators=[InputRequired()],
    )
    months = SelectMultipleField(
        l_('Months'),
        choices=convert_list_to_choices(months),
        validators=[InputRequired()],
    )


class ScheduleExceptionalPeriodForm(PeriodForm):
    destination = DestinationField()


class ScheduleOpenPeriodForm(PeriodForm):
    pass


class ScheduleForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    timezone = SelectField(l_('Timezone'), choices=[])
    closed_destination = DestinationField()
    exceptional_periods = FieldList(FormField(ScheduleExceptionalPeriodForm))
    open_periods = FieldList(FormField(ScheduleOpenPeriodForm))
    submit = SubmitField(l_('Submit'))
