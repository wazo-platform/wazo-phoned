# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import argparse

from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy, parse_config_file
from xivo.xivo_logging import get_log_level_by_name

_DEFAULT_CONFIG = {
    'auth': {
        'host': 'localhost',
        'port': 9497,
        'secret_file': '/etc/xivo-dird-phoned/authentication.yml'
    },
    'dird': {
        'host': 'localhost',
        'port': 9489,
        'default_profile': 'default',
        'verify_certificate': '/usr/share/xivo-certs/server.crt'
    },
    'config_file': '/etc/xivo-dird-phoned/config.yml',
    'extra_config_files': '/etc/xivo-dird-phoned/conf.d/',
    'debug': False,
    'log_level': 'info',
    'log_filename': '/var/log/xivo-dird-phoned.log',
    'foreground': False,
    'pid_filename': '/var/run/xivo-dird-phoned/xivo-dird-phoned.pid',
    'rest_api': {
        'listen': '0.0.0.0',
        'port_http': 9498,
        'port_https': 9499,
        'certificate': '/usr/share/xivo-certs/server.crt',
        'private_key': '/usr/share/xivo-certs/server.key',
        'subnets_authorized': ['127.0.0.1/24'],
        'cors': {
            'enabled': True,
            'allow_headers': 'Content-Type'
        },
    },
    'user': 'www-data',
}


def load(logger, argv):
    cli_config = _parse_cli_args(argv)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    secret = _load_secret_file(ChainMap(cli_config, file_config, _DEFAULT_CONFIG))
    return ChainMap(reinterpreted_config, secret, cli_config, file_config, _DEFAULT_CONFIG)


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config-file',
                        action='store',
                        help="The path where is the config file. Default: %(default)s")
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help="Log debug messages. Overrides log_level. Default: %(default)s")
    parser.add_argument('-f',
                        '--foreground',
                        action='store_true',
                        help="Foreground, don't daemonize. Default: %(default)s")
    parser.add_argument('-l',
                        '--log-level',
                        action='store',
                        help="Logs messages with LOG_LEVEL details. Must be one of:\n"
                             "critical, error, warning, info, debug. Default: %(default)s")
    parser.add_argument('-u',
                        '--user',
                        action='store',
                        help="The owner of the process.")
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


def _load_secret_file(config):
    secret_file = config['auth'].get('secret_file', '')
    secret = parse_config_file(secret_file)['secret']
    return {'auth': {'secret': secret}}


def _get_reinterpreted_raw_values(config):
    result = {}

    log_level = config.get('log_level')
    if log_level:
        result['log_level'] = get_log_level_by_name(log_level)

    return result
