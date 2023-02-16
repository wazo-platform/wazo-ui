# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import IntegerField
from wtforms.validators import (
    InputRequired,
    Length,
    NumberRange,
)

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.destination import DestinationHiddenField, DestinationField


class IvrChoiceForm(BaseForm):
    exten = StringField(validators=[InputRequired(), Length(max=40)])
    destination = DestinationField(destination_label='')


class IvrForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=128)])
    abort_destination = DestinationField(
        destination_label=l_('Abort destination'),
        description=l_(
            'The destination to redirect the caller to when the maximum number of tries is reached.\
                        If not set, the call will be hanged up after playing the abort sound (if set)'
        ),
    )
    abort_sound = SelectField(
        l_('Abort sound'),
        choices=[],
        validators=[Length(max=255)],
        description=l_(
            'The sound played when the caller reach the maximum number of tries.\
                        Not used if an abort destination is set'
        ),
    )
    choices = FieldList(FormField(IvrChoiceForm))
    description = StringField(l_('Description'))
    greeting_sound = SelectField(
        l_('Greeting sound'),
        choices=[],
        validators=[Length(max=255)],
        description=l_('The sound played to greet the caller'),
    )
    invalid_destination = DestinationField(
        destination_label=l_('Invalid destination'),
        description=l_(
            'The destination to redirect the caller to when he choose an invalid option.\
                        If not set, the menu will be replayed'
        ),
    )
    invalid_sound = SelectField(
        l_('Invalid Sound'),
        choices=[],
        validators=[Length(max=255)],
        description=l_(
            'The sound played when the caller choose an invalid option.\
                        Not used if an invalid destination is set'
        ),
    )
    max_tries = IntegerField(
        l_('Max tries'),
        default=3,
        validators=[NumberRange(min=1)],
        description=l_(
            'The maximum number of tries before aborting the call.\
                        Both a timeout and an invalid choice counts toward the number of tries integer Default:3'
        ),
    )
    menu_sound = SelectField(
        l_('Menu Sound'),
        choices=[],
        validators=[Length(max=255)],
        description=l_('The sound played to prompt the caller for input'),
    )
    timeout = IntegerField(
        l_('Timeout'),
        default=5,
        validators=[NumberRange(min=0)],
        description=l_(
            'Number of seconds to wait after the menu sound is played before either replaying the menu,\
                        redirecting the call to the timeout destination (if set) or aborting the call\
                        (if the maximum number of tries has been reached) integer Default:5'
        ),
    )
    timeout_destination = DestinationField(
        destination_label=l_('Timeout destination'),
        description=l_(
            'The destination to redirect the caller to on timeout. If not set, the menu will be replayed'
        ),
    )
    submit = SubmitField(l_('Submit'))

    def to_dict(self):
        data = super().to_dict()

        for field in [
            'abort_destination',
            'invalid_destination',
            'timeout_destination',
        ]:
            if data.get(field, {}).get('type') == 'none':
                data[field] = None
        return data


class IvrDestinationForm(BaseForm):
    set_value_template = '{ivr_name}'

    ivr_id = SelectField(l_('IVR'), validators=[InputRequired()], choices=[])
    ivr_name = DestinationHiddenField()
