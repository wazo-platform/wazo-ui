# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from xivo import plugin_helpers
from .http_server import Server

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
            }
        )

        for core_plugin, config_plugins in config['core_plugins'].items():
            plugin_helpers.load(
                namespace='wazo_ui.core_plugins',
                names={core_plugin: True},
                dependencies={
                    'config_plugins': config_plugins,
                    'flask': self.server.get_app(),
                }
            )

    def run(self):
        logger.info('wazo-ui starting...')
        try:
            self.server.run()
        finally:
            logger.info('wazo-ui stopping...')
