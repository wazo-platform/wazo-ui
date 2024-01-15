# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from xivo import xivo_logging
from xivo.user_rights import change_user

from wazo_ui.config import load as load_config
from wazo_ui.controller import Controller


def main():
    config = load_config(sys.argv[1:])

    if config.get('user'):
        change_user(config['user'])

    xivo_logging.setup_logging(
        config['log_filename'],
        debug=config['debug'],
        log_level=config['log_level'],
    )

    controller = Controller(config)
    controller.run()
