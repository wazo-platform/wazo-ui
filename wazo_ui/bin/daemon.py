# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from xivo import xivo_logging
from xivo.daemonize import pidfile_context
from xivo.user_rights import change_user
from wazo_ui.config import load as load_config
from wazo_ui.controller import Controller

FOREGROUND = True  # Always in foreground systemd takes care of daemonizing


def main():
    config = load_config(sys.argv[1:])

    if config.get('user'):
        change_user(config['user'])

    xivo_logging.setup_logging(config['log_filename'],
                               FOREGROUND,
                               config['debug'],
                               config['log_level'])

    controller = Controller(config)

    with pidfile_context(config['pid_filename'], FOREGROUND):
        controller.run()
