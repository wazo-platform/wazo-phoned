# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import timedelta

import logging
import os

import cherrypy
from babel.core import negotiate_locale
from cherrypy.process.wspbus import states
from cherrypy.process.servers import ServerAdapter
from cheroot import wsgi
from flask import Flask
from flask import request
from flask_babel import Babel
from flask_cors import CORS
from pkg_resources import iter_entry_points, resource_filename, resource_isdir
from werkzeug.contrib.fixers import ProxyFix
from xivo import http_helpers
from xivo.http_helpers import ReverseProxied

VERSION = 0.1
BABEL_DEFAULT_LOCALE = 'en'
TRANSLATION_DIRECTORY = 'translations'

logger = logging.getLogger(__name__)
cherrypy.engine.signal_handler.set_handler('SIGTERM', cherrypy.engine.exit)


class HTTPServer:
    def __init__(self, config):
        self.config = config['rest_api']
        self.app = Flask('wazo_phoned')
        self._configure_babel(config['enabled_plugins'])
        http_helpers.add_logger(self.app, logger)
        self.app.before_request(http_helpers.log_before_request)
        self.app.after_request(http_helpers.log_request)
        self.app.secret_key = os.urandom(24)
        self.app.permanent_session_lifetime = timedelta(minutes=5)
        self.load_cors()

    def load_cors(self):
        cors_config = dict(self.config.get('cors', {}))
        enabled = cors_config.pop('enabled', False)
        if enabled:
            CORS(self.app, **cors_config)

    def _configure_babel(self, enabled_plugins):
        self.babel = Babel(self.app)
        self.app.config['BABEL_DEFAULT_LOCALE'] = BABEL_DEFAULT_LOCALE
        self.app.config['BABEL_TRANSLATION_DIRECTORIES'] = ';'.join(
            self._get_translation_directories(enabled_plugins)
        )

        @self.babel.localeselector
        def get_locale():
            translations = set(
                [str(locale) for locale in self.babel.list_translations()]
            )
            translations.add(BABEL_DEFAULT_LOCALE)
            logger.debug('Available translations: %s', translations)
            logger.debug('accept_languages: %s', request.accept_languages)
            preferred = [
                locale.replace('-', '_') for locale in request.accept_languages.values()
            ]
            best_match = negotiate_locale(preferred, translations)
            logger.debug('Best locale match: %s', best_match)
            return best_match

    def _get_translation_directories(self, enabled_plugins):
        main_translation_directory = 'translations'
        result = [main_translation_directory]
        entry_points = (
            e
            for e in iter_entry_points(group='wazo_phoned.plugins')
            if e.name in enabled_plugins
        )
        for ep in entry_points:
            if resource_isdir(ep.module_name, TRANSLATION_DIRECTORY):
                result.append(resource_filename(ep.module_name, TRANSLATION_DIRECTORY))
        return result

    def run(self):
        http_config = self.config['http']
        https_config = self.config['https']

        wsgi_app = ReverseProxied(
            ProxyFix(wsgi.WSGIPathInfoDispatcher({'/': self.app}))
        )
        cherrypy.server.unsubscribe()
        cherrypy.config.update({'environment': 'production'})

        if https_config['enabled']:
            try:
                bind_addr_https = (https_config['listen'], https_config['port'])
                server_https = wsgi.WSGIServer(
                    bind_addr=bind_addr_https, wsgi_app=wsgi_app
                )
                server_https.ssl_adapter = http_helpers.ssl_adapter(
                    https_config['certificate'], https_config['private_key']
                )

                ServerAdapter(cherrypy.engine, server_https).subscribe()
                logger.debug(
                    'WSGIServer starting... uid: %s, listen: %s:%s',
                    os.getuid(),
                    bind_addr_https[0],
                    bind_addr_https[1],
                )
            except IOError as e:
                logger.warning("HTTPS server won't start: %s", e)
        else:
            logger.debug('HTTPS server is disabled')

        if http_config['enabled']:
            bind_addr_http = (http_config['listen'], http_config['port'])
            server_http = wsgi.WSGIServer(bind_addr=bind_addr_http, wsgi_app=wsgi_app)
            ServerAdapter(cherrypy.engine, server_http).subscribe()
            logger.debug(
                'WSGIServer starting... uid: %s, listen: %s:%s',
                os.getuid(),
                bind_addr_http[0],
                bind_addr_http[1],
            )
        else:
            logger.debug('HTTP server is disabled')

        if not http_config['enabled'] and not https_config['enabled']:
            logger.critical('No HTTP/HTTPS server enabled')
            exit()

        list_routes(self.app)

        try:
            cherrypy.engine.start()
            cherrypy.engine.wait(states.EXITING)
        except KeyboardInterrupt:
            logger.warning('Stopping wazo-phoned: KeyboardInterrupt')
            cherrypy.engine.exit()

    def stop(self):
        cherrypy.engine.exit()

    def join(self):
        if cherrypy.engine.state == states.EXITING:
            cherrypy.engine.block()


def list_routes(app):
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, rule)
        output.append(line)

    for line in sorted(output):
        logger.debug(line)
