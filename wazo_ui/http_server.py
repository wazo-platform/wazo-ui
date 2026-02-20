# Copyright 2018-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
from datetime import timedelta
from importlib.metadata import entry_points
from importlib.resources import files

import requests
from flask import Flask, request, session, url_for
from flask_babel import Babel
from flask_login import LoginManager
from flask_menu import Menu
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from requests.exceptions import HTTPError
from wazo_auth_client import Client as AuthClient
from werkzeug.middleware.proxy_fix import ProxyFix
from xivo import http_helpers, wsgi
from xivo.http_helpers import ReverseProxied

from .errors import configure_error_handlers
from .user import UserUI

TRANSLATION_DIRECTORY = 'translations'
BABEL_DEFAULT_LOCALE = 'en'
HOME = '/var/lib/wazo-ui'

logger = logging.getLogger(__name__)
app = Flask('wazo_ui')


class Server:
    def __init__(self, global_config):
        self.config = global_config['http']
        http_helpers.add_logger(app, logger)

        app.after_request(http_helpers.log_request_hide_token)

        app.secret_key = os.urandom(24)
        app.permanent_session_lifetime = timedelta(
            seconds=global_config['session_lifetime']
        )
        app.config['amid'] = global_config.get('amid', {})
        app.config['auth'] = global_config.get('auth', {})
        app.config['call-logd'] = global_config.get('call-logd', {})
        app.config['confd'] = global_config.get('confd', {})
        app.config['dird'] = global_config.get('dird', {})
        app.config['plugind'] = global_config.get('plugind', {})
        app.config['provd'] = global_config.get('provd', {})
        app.config['webhookd'] = global_config.get('webhookd', {})
        app.config['websocketd'] = global_config.get('websocketd', {})
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 megabytes

        if global_config['debug']:
            app.jinja_env.auto_reload = True
            app.config['TEMPLATES_AUTO_RELOAD'] = True

        configure_error_handlers(app)
        self._override_url_for()
        self._configure_jinja()
        self._configure_login(app.config['auth'])
        self._configure_menu()
        self._configure_session()
        self._configure_babel(global_config['enabled_plugins'])

    def get_app(self):
        return app

    def run(self):
        bind_addr = (self.config['listen'], self.config['port'])

        wsgi_app = ReverseProxied(ProxyFix(wsgi.WSGIPathInfoDispatcher({'/': app})))
        self.server = wsgi.WSGIServer(bind_addr=bind_addr, wsgi_app=wsgi_app)
        if self.config['certificate'] and self.config['private_key']:
            logger.warning(
                'Using service SSL configuration is deprecated. Please use NGINX instead.'
            )
            self.server.ssl_adapter = http_helpers.ssl_adapter(
                self.config['certificate'], self.config['private_key']
            )
        logger.debug(
            'WSGIServer starting... uid: %s, listen: %s:%s',
            os.getuid(),
            bind_addr[0],
            bind_addr[1],
        )
        for route in http_helpers.list_routes(app):
            logger.debug(route)

        self.server.start()

    def stop(self):
        if self.server:
            self.server.stop()

    def _override_url_for(self):
        def url_for_allow_empty_endpoint(endpoint, **values):
            if not endpoint:
                return ''
            return url_for(endpoint, **values)

        @app.context_processor
        def override_url_for():
            return dict(url_for=url_for_allow_empty_endpoint)

    def _configure_jinja(self):
        app.jinja_env.trim_blocks = True
        app.jinja_env.add_extension('jinja2.ext.do')

    def _configure_login(self, auth_config):
        login_manager = LoginManager()
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_token(token):
            try:
                response = AuthClient(**auth_config).token.get(token)
            except HTTPError:
                return None
            except requests.ConnectionError:
                logger.warning('Wazo authentication server connection error')
                return None
            token = response.get('token')
            if not token:
                return None
            return UserUI(token, response.get('auth_id'))

    def _configure_menu(self):
        Menu(app=app)

    def _configure_babel(self, enabled_plugins):
        babel = Babel()
        babel.init_app(app)
        app.config['BABEL_DEFAULT_LOCALE'] = BABEL_DEFAULT_LOCALE
        app.config['BABEL_TRANSLATION_DIRECTORIES'] = ';'.join(
            self._get_translation_directories(enabled_plugins)
        )

        @babel.localeselector
        def get_locale():
            if not session.get('language'):
                translations = {locale.language for locale in babel.list_translations()}
                translations.add(BABEL_DEFAULT_LOCALE)

                session['language'] = request.accept_languages.best_match(translations)

            return session['language']

    def _get_translation_directories(self, enabled_plugins):
        main_translation_directory = 'translations'
        result = [main_translation_directory]
        eps = (
            e
            for e in entry_points(group='wazo_ui.plugins')
            if e.name in enabled_plugins
        )
        for ep in eps:
            # e.g. 'wazo_ui.plugins.user.plugin:Plugin' -> 'wazo_ui.plugins.user'
            package_name = ep.value.split(':')[0].rsplit('.', 1)[0]
            translation_path = files(package_name) / TRANSLATION_DIRECTORY
            if translation_path.is_dir():
                result.append(str(translation_path))
        return result

    def _configure_session(self):
        app.config['SESSION_TYPE'] = 'sqlalchemy'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{HOME}/sessions.db'
        db = SQLAlchemy(app)
        app.config['SESSION_SQLALCHEMY'] = db
        flask_session = Session()
        flask_session.init_app(app)
        with app.app_context():
            db.create_all()
