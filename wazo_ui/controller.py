# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from flask_babel import lazy_gettext as l_

from xivo import plugin_helpers
from .http_server import Server
from wazo_ui.helpers.destination import register_destination_form
from wazo_ui.helpers.error import (
    ErrorExtractor,
    ErrorTranslator,
    ConfdErrorExtractor,
    URL_TO_NAME_RESOURCES,
    RESOURCES,
    GENERIC_PATTERN_ERRORS,
    SPECIFIC_PATTERN_ERRORS
)

from wazo_ui.core.client import engine_clients
from wazo_ui.core.form import (
    ApplicationDestination,
    ApplicationCallBackDISADestination,
    ApplicationDISADestination,
    ApplicationDirectoryDestination,
    ApplicationFaxToMailDestination,
    ApplicationVoicemailDestination,
    CustomDestination,
    HangupDestination,
    NoneDestination,
    register_destination_form_application,
)

logger = logging.getLogger(__name__)


class Controller():

    def __init__(self, config):
        self.server = Server(config)
        plugin_helpers.load(
            namespace='wazo_ui.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'config': config,
                'flask': self.server.get_app(),
                'clients': engine_clients
            }
        )

        ErrorExtractor.register_url_to_name_resources(URL_TO_NAME_RESOURCES)
        ErrorTranslator.register_resources(RESOURCES)

        ConfdErrorExtractor.register_generic_patterns(GENERIC_PATTERN_ERRORS)
        ConfdErrorExtractor.register_specific_patterns(SPECIFIC_PATTERN_ERRORS)

        register_destination_form('application', l_('Application'), ApplicationDestination)
        register_destination_form('hangup', l_('Hangup'), HangupDestination)
        register_destination_form('custom', l_('Custom'), CustomDestination)
        register_destination_form('none', l_('None'), NoneDestination, position=0)

        register_destination_form_application(
            'callback_disa', l_('CallBack DISA'),
            ApplicationCallBackDISADestination,
        )
        register_destination_form_application(
            'directory', l_('Directory'),
            ApplicationDirectoryDestination,
        )
        register_destination_form_application(
            'disa', l_('DISA'),
            ApplicationDISADestination,
        )
        register_destination_form_application(
            'fax_to_mail', l_('Fax to Mail'),
            ApplicationFaxToMailDestination,
        )
        register_destination_form_application(
            'voicemail', l_('Voicemail'),
            ApplicationVoicemailDestination,
        )

    def run(self):
        logger.info('wazo-ui starting...')
        try:
            self.server.run()
        finally:
            logger.info('wazo-ui stopping...')
