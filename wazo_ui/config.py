# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse

from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy
from xivo.xivo_logging import get_log_level_by_name

_DEFAULT_CONFIG = {
    'config_file': '/etc/wazo-ui/config.yml',
    'extra_config_files': '/etc/wazo-ui/conf.d',
    'debug': False,
    'foreground': False,
    'log_level': 'info',
    'log_filename': '/var/log/wazo-ui.log',
    'pid_filename': '/var/run/wazo-ui/wazo-ui.pid',
    'session_file_dir': '/var/lib/wazo-ui/sessions',
    'session_lifetime': 3600,
    'https': {
        'listen': '0.0.0.0',
        'port': 9296,
        'certificate': '/usr/share/xivo-certs/server.crt',
        'private_key': '/usr/share/xivo-certs/server.key',
    },
    'auth': {
        'host': '127.0.0.1',
        'port': 443,
        'verify_certificate': '/usr/share/xivo-certs/server.crt',
    },
    'confd': {
        'host': 'localhost',
        'port': 9486,
        'verify_certificate': '/usr/share/xivo-certs/server.crt',
    },
    'enabled_plugins': {
        'authentication': True,
        'index': True
    },
    'core_plugins': {}
}


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config-file',
                        action='store',
                        help='The path to the config file. Default %(default)s')
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Log debug messages. Default %(default)s')
    parser.add_argument('-f',
                        '--foreground',
                        action='store_true',
                        help="Foreground, don't daemonize. Default %(default)s")
    parser.add_argument('-l',
                        '--log-level',
                        action='store',
                        help="Logs messages with LOG_LEVEL details. Must be one of:\n"
                             "critical, error, warning, info, debug. Default: %(default)s")
    parser.add_argument('-u',
                        '--user',
                        action='store',
                        help='The owner of the process')
    parsed_args = parser.parse_args(argv)

    result = {}
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        result['debug'] = parsed_args.debug
    if parsed_args.foreground:
        result['foreground'] = parsed_args.foreground
    if parsed_args.log_level:
        result['log_level'] = parsed_args.log_level
    if parsed_args.user:
        result['user'] = parsed_args.user

    return result


def _get_reinterpreted_raw_values(config):
    result = {}

    log_level = config.get('log_level')
    if log_level:
        result['log_level'] = get_log_level_by_name(log_level)

    return result


def load(argv):
    cli_config = _parse_cli_args(argv)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    return ChainMap(reinterpreted_config, cli_config, file_config, _DEFAULT_CONFIG)
