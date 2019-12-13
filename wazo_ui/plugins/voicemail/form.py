# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    HiddenField,
    SubmitField,
    StringField,
    SelectField,
    BooleanField
)
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange, Regexp

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.destination import DestinationHiddenField


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class VoicemailForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=80)])
    context = SelectField(l_('Context'), [InputRequired()], choices=[])
    number = StringField(l_('Number'), [InputRequired(), Length(max=40), Regexp(r'^[0-9]+$')])
    email = EmailField(l_('Email'), validators=[Length(max=80)])
    password = StringField(l_('Password'), [Length(max=80), Regexp(r'^[0-9]+$')], render_kw={'type': 'password',
                                                                                             'data_toggle': 'password'})
    timezone = SelectField(
        l_('Timezone'),
        validators=[InputRequired()],
        choices=[
            ('na-newfoundland', 'America/St_Johns'),
            ('na-atlantic', 'America/Halifax'),
            ('na-eastern', 'America/New_York'),
            ('na-central', 'America/Chicago'),
            ('na-mountain', 'America/Denver'),
            ('na-pacific', 'America/Los_Angeles'),
            ('na-alaska', 'America/Anchorage'),
            ('eu-fr', 'Europe/Paris')
        ]
    )
    language = SelectField(
        l_('Language'),
        validators=[InputRequired()],
        choices=[
            ('fr_FR', l_('French')),
            ('fr_CA', l_('French Canadian')),
            ('en_US', l_('English')),
        ]
    )
    users = FieldList(FormField(UserForm))
    user_uuid = SelectField(l_('Users'), choices=[])
    max_messages = IntegerField(l_('Maximum messages'), [NumberRange(min=0)])
    ask_password = BooleanField(l_('Ask for password'), default=False)
    attach_audio = BooleanField(l_('Attach audio'), default=False)
    delete_messages = BooleanField(l_('Delete message after notification'), default=False)
    enabled = BooleanField(l_('Activated'))
    submit = SubmitField(l_('Submit'))


class VoicemailDestinationForm(BaseForm):
    set_value_template = '{voicemail_name}'

    voicemail_id = SelectField(l_('Voicemail'), [InputRequired()], choices=[])
    greeting = SelectField(
        l_('Greeting'), choices=[
            ('', l_('None')),
            ('busy', l_('Busy')),
            ('unavailable', l_('Unavailable')),
        ]
    )
    skip_instructions = BooleanField(l_('Skip instructions'))
    voicemail_name = DestinationHiddenField()
