# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import EmailField, FormField, IntegerField, SelectField, StringField
from wtforms.validators import InputRequired, Length, NumberRange, Regexp

from wazo_ui.helpers.destination import BaseDestinationForm
from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.view import listing_urls

_application_destination_choices = []


def register_destination_form_application(type_id, type_label, form, position=-1):
    if (type_id, type_label) not in _application_destination_choices:
        _application_destination_choices.insert(position, (type_id, type_label))
    setattr(ApplicationDestination, type_id, FormField(form))


class HangupCongestionDestination(BaseForm):
    timeout = IntegerField(l_('Timeout'), [NumberRange(min=0)])


class HangupBusyDestination(BaseForm):
    timeout = IntegerField(l_('Timeout'), [NumberRange(min=0)])


class HangupNormalDestination(BaseForm):
    pass


class HangupDestination(BaseDestinationForm):
    select_field = 'cause'

    cause = SelectField(
        l_('Cause'),
        choices=[
            ('normal', l_('Normal')),
            ('busy', l_('Busy')),
            ('congestion', l_('Congestion')),
        ],
    )
    busy = FormField(HangupBusyDestination)
    congestion = FormField(HangupBusyDestination)
    normal = FormField(HangupNormalDestination)


class ApplicationCallBackDISADestination(BaseForm):
    pin = StringField(
        l_('PIN'),
        [Length(max=40), Regexp(r'^[0-9]+$')],
        render_kw={'type': 'password'},
    )
    context = StringField(
        l_('Context'), [InputRequired(), Length(max=79), Regexp(r'^[a-zA-Z0-9_-]+$')]
    )


class ApplicationDISADestination(ApplicationCallBackDISADestination):
    pass


class ApplicationDirectoryDestination(BaseForm):
    context = StringField(
        l_('Context'), [InputRequired(), Length(max=79), Regexp(r'^[a-zA-Z0-9_-]+$')]
    )


class ApplicationFaxToMailDestination(BaseForm):
    email = EmailField(l_('Email'), [InputRequired(), Length(max=80)])


class ApplicationVoicemailDestination(BaseForm):
    context = StringField(
        l_('Context'), [InputRequired(), Length(max=79), Regexp(r'^[a-zA-Z0-9_-]+$')]
    )


class ApplicationDestination(BaseDestinationForm):
    select_field = 'application'

    application = SelectField(l_('Application'), choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.application.choices = _application_destination_choices
        self.listing_urls = listing_urls


class CustomDestination(BaseForm):
    command = StringField(validators=[InputRequired(), Length(max=255)])


class NoneDestination(BaseForm):
    pass
