# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse

from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy
from xivo.xivo_logging import get_log_level_by_name

_DEFAULT_CONFIG = {
    'config_file': '/etc/wazo-ui/config.yml',
    'extra_config_files': '/etc/wazo-ui/conf.d',
    'debug': False,
    'log_level': 'info',
    'log_filename': '/var/log/wazo-ui.log',
    'session_lifetime': 60 * 60 * 8,
    'http': {
        'listen': '127.0.0.1',
        'port': 9296,
        'certificate': None,
        'private_key': None,
    },
    'amid': {
        'host': 'localhost',
        'port': 9491,
        'prefix': None,
        'https': False,
    },
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
    },
    'call-logd': {
        'host': 'localhost',
        'port': 9298,
        'prefix': None,
        'https': False,
    },
    'confd': {
        'host': 'localhost',
        'port': 9486,
        'prefix': None,
        'https': False,
    },
    'dird': {
        'host': 'localhost',
        'port': 9489,
        'prefix': None,
        'https': False,
    },
    'plugind': {
        'host': 'localhost',
        'port': 9503,
        'prefix': None,
        'https': False,
    },
    'provd': {
        'host': 'localhost',
        'port': 8666,
        'prefix': None,
        'https': False,
    },
    'webhookd': {
        'host': 'localhost',
        'port': 9300,
        'prefix': None,
        'https': False,
    },
    # Information for websocketd are used by the client browser
    'websocketd': {
        'host': None,
        'port': 443,
        'prefix': '/api/websocketd',
        'verify_certificate': False,
    },
    'enabled_plugins': {
        'access_feature': True,
        'authentication': True,
        'index': True,
        'application': True,
        'agent': True,
        'cli': True,
        'call_filter': True,
        'call_permission': True,
        'call_pickup': True,
        'cdr': True,
        'conference': True,
        'context': True,
        'device': True,
        'dird_profile': True,
        'dird_source': True,
        'dhcp': True,
        'extension': True,
        'external_auth': True,
        'funckey': True,
        'general_settings': True,
        'group': True,
        'global_settings': True,
        'ha': True,
        'hep': True,
        'identity': True,
        'incall': True,
        'ivr': True,
        'line': True,
        'moh': True,
        'outcall': True,
        'paging': True,
        'parking_lot': True,
        'phonebook': True,
        'phone_number': True,
        'plugin': True,
        'provisioning': True,
        'queue': True,
        'recording_announcement': True,
        'rtp': True,
        'schedule': True,
        'sip_template': True,
        'skill': True,
        'skillrule': True,
        'sound': True,
        'switchboard': True,
        'transport': True,
        'trunk': True,
        'user': True,
        'voicemail': True,
        'webhook': True,
    },
}


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config-file',
        action='store',
        help='The path to the config file. Default %(default)s',
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Log debug messages. Default %(default)s',
    )
    parser.add_argument(
        '-l',
        '--log-level',
        action='store',
        help="Logs messages with LOG_LEVEL details. Must be one of:\n"
        "critical, error, warning, info, debug. Default: %(default)s",
    )
    parser.add_argument('-u', '--user', action='store', help='The owner of the process')
    parsed_args = parser.parse_args(argv)

    result = {}
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        result['debug'] = parsed_args.debug
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
    reinterpreted_config = _get_reinterpreted_raw_values(
        ChainMap(cli_config, file_config, _DEFAULT_CONFIG)
    )
    return ChainMap(reinterpreted_config, cli_config, file_config, _DEFAULT_CONFIG)
