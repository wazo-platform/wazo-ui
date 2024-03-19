# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FormField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.utils import unset_value
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.destination import BaseDestinationForm, DestinationHiddenField
from wazo_ui.helpers.form import BaseForm

_application_destination_choices = []


def register_application_destination_form(type_id, type_label, form, position=-1):
    if (type_id, type_label) in _application_destination_choices:
        return
    _application_destination_choices.insert(position, (type_id, type_label))
    setattr(ApplicationDestinationForm, type_id, FormField(form))


class ApplicationDestinationForm(BaseDestinationForm):
    select_field = 'destination'

    destination = SelectField(l_('Destination'), choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destination.choices = _application_destination_choices

    def to_dict(self):
        result = super().to_dict()
        selected_value = result.get(self.select_field)
        if selected_value == 'None':
            result[self.select_field] = None
        return result


class ApplicationDestinationField(FormField):
    def __init__(self, *args, **kwargs):
        self.destination_label = kwargs.pop('destination_label', None)
        self.destination_form = kwargs.pop(
            'destination_form', ApplicationDestinationForm
        )
        super().__init__(self.destination_form, *args, **kwargs)

    def process(self, formdata, data=unset_value):
        super().process(formdata, data)
        if self.destination_label is not None:
            self.form.destination.label.text = self.destination_label


class ApplicationForm(BaseForm):
    name = StringField(l_('Name'), [Length(max=128)])
    destination = ApplicationDestinationField()

    submit = SubmitField(l_('Submit'))


class NodeDestinationForm(BaseForm):
    type = SelectField(
        l_('Type'),
        choices=[
            ('holding', l_('Holding')),
        ],
    )
    music_on_hold = StringField(l_('Music On Hold'))
    answer = BooleanField(l_('Answer'), default=False)


class NoneDestinationForm(BaseForm):
    pass


class ApplicationCustomDestination(BaseForm):
    set_value_template = '{application_name}'

    application_uuid = SelectField(l_('Application'), [InputRequired()], choices=[])
    application_name = DestinationHiddenField()
