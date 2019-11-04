# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import Blueprint
from flask_restful import Api

from wazo_phoned.http_server import VERSION


def create_blueprint_api(app, name, import_name):
    api_blueprint = Blueprint(name, import_name, template_folder='templates')
    api = Api(api_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/{}'.format(VERSION))
    return api
