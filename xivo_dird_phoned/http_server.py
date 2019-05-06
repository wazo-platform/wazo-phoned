# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import timedelta

import logging
import os

import cherrypy
from cherrypy.process.wspbus import states
from cherrypy.process.servers import ServerAdapter
from cheroot import wsgi
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from xivo import http_helpers

VERSION = 0.1

logger = logging.getLogger(__name__)
api = Api(prefix='/{}'.format(VERSION))
cherrypy.engine.signal_handler.set_handler('SIGTERM', cherrypy.engine.exit)


class HTTPServer:

    def __init__(self, config):
        self.config = config
        self.app = Flask('xivo_dird_phoned')
        http_helpers.add_logger(self.app, logger)
        self.app.before_request(http_helpers.log_before_request)
        self.app.after_request(http_helpers.log_request)
        self.app.secret_key = os.urandom(24)
        self.app.permanent_session_lifetime = timedelta(minutes=5)
        self.load_cors()
        self.api = api

    def load_cors(self):
        cors_config = dict(self.config.get('cors', {}))
        enabled = cors_config.pop('enabled', False)
        if enabled:
            CORS(self.app, **cors_config)

    def run(self):
        self.api.init_app(self.app)
        http_config = self.config['http']
        https_config = self.config['https']

        wsgi_app = wsgi.WSGIPathInfoDispatcher({'/': self.app})
        cherrypy.server.unsubscribe()
        cherrypy.config.update({'environment': 'production'})

        if https_config['enabled']:
            try:
                bind_addr_https = (https_config['listen'], https_config['port'])
                server_https = wsgi.WSGIServer(bind_addr=bind_addr_https, wsgi_app=wsgi_app)
                server_https.ssl_adapter = http_helpers.ssl_adapter(
                    https_config['certificate'],
                    https_config['private_key'],
                )

                ServerAdapter(cherrypy.engine, server_https).subscribe()
                logger.debug(
                    'WSGIServer starting... uid: %s, listen: %s:%s',
                    os.getuid(), bind_addr_https[0], bind_addr_https[1],
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
                os.getuid(), bind_addr_http[0], bind_addr_http[1],
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
            logger.warning('Stopping xivo-dird-phoned: KeyboardInterrupt')
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
