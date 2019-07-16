# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import traceback

from flask import redirect
from flask import url_for
from flask.helpers import flash
from requests.exceptions import ConnectionError
from flask_login import current_user

from .helpers.error import (
    ErrorTranslator,
    GENERIC_MESSAGE_ERRORS,
    SPECIFIC_MESSAGE_ERRORS
)


logger = logging.getLogger(__name__)


def configure_error_handlers(app):

    ErrorTranslator.register_generic_messages(GENERIC_MESSAGE_ERRORS)
    ErrorTranslator.register_specific_messages(SPECIFIC_MESSAGE_ERRORS)

    @app.errorhandler(401)
    def page_unauthorized(error):
        flash(str(error), 'error')
        return redirect(url_for('login.Login:get'))

    @app.errorhandler(403)
    def page_forbidden(error):
        return _flash_and_redirect(error)

    @app.errorhandler(404)
    def page_not_found(error):
        logger.warning(error)
        logger.warning(traceback.format_exc())
        return _flash_and_redirect(error)

    @app.errorhandler(ConnectionError)
    def connection_error(error):
        logger.exception(error)
        return _flash_and_redirect(error)

    @app.errorhandler(Exception)
    def exception_handler(error):
        logger.exception('Unexpected error:')
        return _flash_and_redirect(error)

    def _flash_and_redirect(error):
        if error:
            flash(str(error), 'error')
        return redirect(current_user.get_user_index_url() if current_user.is_authenticated else url_for('login.Login:get'))
