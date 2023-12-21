# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FormField,
    HiddenField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import InputRequired
from wtforms.widgets import PasswordInput

from wazo_ui.helpers.form import BaseForm


class MicrosoftForm(BaseForm):
    client_id = StringField(l_('Client ID'), validators=[InputRequired()])
    client_secret = StringField(
        l_('Client secret'), widget=PasswordInput(hide_value=False)
    )


class GoogleForm(BaseForm):
    client_id = StringField(l_('Client ID'), validators=[InputRequired()])
    client_secret = StringField(
        l_('Client secret'), widget=PasswordInput(hide_value=False)
    )


class MobileForm(BaseForm):
    fcm_api_key = StringField(
        l_('Firebase Cloud Messaging Api Key'), widget=PasswordInput(hide_value=False)
    )
    fcm_sender_id = StringField(
        l_('Firebase Cloud Messaging Sender ID'), widget=PasswordInput(hide_value=False)
    )
    ios_apn_certificate = TextAreaField(l_('Ios APN Certificate'))
    ios_apn_private = TextAreaField(l_('Ios APN Private certificate'))
    is_sandbox = BooleanField(l_('Use sandbox'))


class ExternalAuthForm(BaseForm):
    type = HiddenField()
    editing = HiddenField()
    microsoft_config = FormField(MicrosoftForm)
    google_config = FormField(GoogleForm)
    mobile_config = FormField(MobileForm)
    submit = SubmitField()
