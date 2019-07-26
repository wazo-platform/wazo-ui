# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import requests

from flask import url_for, render_template, redirect, session
from flask_babel import Locale, get_locale
from flask_classful import FlaskView
from flask_login import login_user, logout_user, current_user

from wazo_ui.helpers.client import auth_client
from wazo_ui.helpers.menu import init_visualization
from wazo_ui.helpers import instance as instance_helper
from wazo_ui.http_server import app

from .form import LoginForm

logger = logging.getLogger(__name__)


class Login(FlaskView):
    babel = None

    def get(self):
        return self._login()

    def post(self):
        return self._login()

    def _login(self):
        if current_user.is_authenticated:
            self._connect_to_instance(current_user)
            return redirect(current_user.get_user_index_url())

        form = LoginForm()
        form.language.choices = self._build_language_list()
        if form.validate_on_submit():
            if not form.csrf_token.validate(form):
                return render_template('authentication/login.html', form=form)

            session['language'] = form.language.data
            login_user(form.user)
            init_visualization()

            self._connect_to_instance(form.user)

            return redirect(current_user.get_user_index_url())

        return render_template('authentication/login.html', form=form)

    def _build_language_list(self):
        default_locale = Locale.parse(self.babel.app.config['BABEL_DEFAULT_LOCALE'])
        session_locale = get_locale()
        first_choice = (session_locale.language, session_locale.language_name)

        choices = set(((l.language, l.language_name) for l in self.babel.list_translations()))
        choices.add(first_choice)
        choices.add((default_locale.language, default_locale.language_name))
        choices.remove(first_choice)

        return [first_choice] + list(choices)

    def _connect_to_instance(self, user):
        raw_user = user.get_user()

        instance_helper.instance_connect_from_credential({
            'instance': {
                'remote_host': app.config['auth']['host'],
                'https_port': 443,
                'uuid': raw_user['instance_uuid'],
                'tenant_uuid': raw_user['instance_uuid'],
                'service_id': 1,
                'name': None
            },
            'username': raw_user['username'],
            'password': raw_user['password'],
        })


class Logout(FlaskView):

    def get(self):
        token = current_user.get_id()
        current_user.reset_instance()
        try:
            auth_client.token.revoke(token)
        except requests.HTTPError as e:
            logger.warning('Error with Wazo authentication server: %(error)s', error=e.message)
        except requests.ConnectionError:
            logger.warning('Wazo authentication server connection error: Unable to revoke token')
        session.clear()
        logout_user()
        return redirect(url_for('login.Login:get'))
