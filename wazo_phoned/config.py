# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse

from xivo.chain_map import ChainMap
from xivo.config_helper import parse_config_file, read_config_file_hierarchy
from xivo.xivo_logging import get_log_level_by_name

_DEFAULT_CONFIG = {
    'config_file': '/etc/wazo-phoned/config.yml',
    'extra_config_files': '/etc/wazo-phoned/conf.d/',
    'debug': False,
    'log_level': 'info',
    'user': 'www-data',
    'log_filename': '/var/log/wazo-phoned.log',
    'rest_api': {
        'http': {'listen': '0.0.0.0', 'port': 9498, 'enable': True},
        'https': {
            'listen': '0.0.0.0',
            'port': 9499,
            'enable': True,
            'certificate': '/usr/share/wazo-certs/server.crt',
            'private_key': '/usr/share/wazo-certs/server.key',
        },
        'authorized_subnets': ['127.0.0.1/24'],
        'cors': {'enabled': True, 'allow_headers': ['Content-Type']},
        'max_threads': 10,
    },
    'bus': {
        'username': 'guest',
        'password': 'guest',
        'host': 'localhost',
        'port': 5672,
        'subscribe_exchange_name': 'wazo-headers',
        'subscribe_exchange_type': 'headers',
    },
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'prefix': None,
        'https': False,
        'key_file': '/var/lib/wazo-auth-keys/wazo-phoned-key.yml',
    },
    'dird': {'host': 'localhost', 'port': 9489, 'prefix': None, 'https': False},
    'amid': {'host': 'localhost', 'port': 9491, 'prefix': None, 'https': False},
    'confd': {'host': 'localhost', 'port': 9486, 'prefix': None, 'https': False},
    'enabled_plugins': {
        'aastra': True,
        'blf': True,
        'api': True,
        'cisco': True,
        'config': True,
        'endpoint': True,
        'fanvil': True,
        'gigaset': True,
        'htek': True,
        'polycom': True,
        'snom': True,
        'status': True,
        'thomson': True,
        'yealink': True,
    },
}


def load(logger, argv):
    cli_config = _parse_cli_args(argv)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(
        ChainMap(cli_config, file_config, _DEFAULT_CONFIG)
    )
    service_key = _load_key_file(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    return ChainMap(
        reinterpreted_config, cli_config, service_key, file_config, _DEFAULT_CONFIG
    )


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config-file',
        action='store',
        help="The path where is the config file. Default: %(default)s",
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help="Log debug messages. Overrides log_level. Default: %(default)s",
    )
    parser.add_argument(
        '-l',
        '--log-level',
        action='store',
        help="Logs messages with LOG_LEVEL details. Must be one of:\n"
        "critical, error, warning, info, debug. Default: %(default)s",
    )
    parser.add_argument(
        '-u', '--user', action='store', help="The owner of the process."
    )
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


def _load_key_file(config):
    key_file = parse_config_file(config['auth']['key_file'])
    return {
        'auth': {
            'username': key_file['service_id'],
            'password': key_file['service_key'],
        }
    }


def _get_reinterpreted_raw_values(config):
    result = {}

    log_level = config.get('log_level')
    if log_level:
        result['log_level'] = get_log_level_by_name(log_level)

    return result
