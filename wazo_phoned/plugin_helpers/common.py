# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import Blueprint
from flask_restful import Api
from time import time

from wazo_phoned.http_server import VERSION


def output_error(code, msg):
    return {'reason': [msg], 'timestamp': [time()], 'status_code': code}, code


def create_blueprint_api(app, name, import_name):
    api_blueprint = Blueprint(name, import_name, template_folder='templates')
    api = Api(api_blueprint)
    app.register_blueprint(api_blueprint, url_prefix=f'/{VERSION}')
    return api
