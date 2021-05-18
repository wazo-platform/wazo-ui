# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests
import logging

from requests.exceptions import HTTPError

from flask import session
from flask_babel import lazy_gettext as l_
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, ValidationError

from wazo_auth_client import Client as AuthClient
from wazo_ui.http_server import app
from wazo_ui.user import UserUI

USERNAME_PASSWORD_ERROR = l_('Wrong username and/or password')

logger = logging.getLogger(__name__)


def unauthorized(error):
    return error.response is not None and error.response.status_code == 401


class LoginForm(FlaskForm):

    username = StringField(l_('Username'), validators=[InputRequired()])
    password = PasswordField(l_('Password'), validators=[InputRequired()])
    language = SelectField(l_('Language'))
    submit = SubmitField(l_('Login'), render_kw={'data-loading-text': "<i class='fa fa-circle-o-notch fa-spin'></i> Processing..."})

    def validate(self):
        super().validate()
        try:
            auth_client = AuthClient(
                username=self.username.data,
                password=self.password.data,
                **app.config['auth'],
            )
            response = auth_client.token.new(expiration=60 * 60 * 12)
            auth_client.set_token(response['token'])
            user = auth_client.users.get(response['metadata']['uuid'])
            user['password'] = self.password.data
            user['instance_uuid'] = response['xivo_uuid']
            session['user'] = user
        except HTTPError as e:
            if unauthorized(e):
                self.username.errors.append(USERNAME_PASSWORD_ERROR)
                self.password.errors.append(USERNAME_PASSWORD_ERROR)
                return False
            raise ValidationError(l_('Error with Wazo authentication server: %(error)s', error=e.message))
        except requests.ConnectionError:
            raise ValidationError(l_('Wazo authentication server connection error'))

        self.user = UserUI(response['token'], response['auth_id'])
        self.user.set_instance_config(app.config)

        return True
