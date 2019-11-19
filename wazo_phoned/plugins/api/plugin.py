# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .http import OpenAPIResource
from wazo_phoned.plugin_helpers.common import create_blueprint_api


class Plugin:
    def load(self, dependencies):
        app = dependencies['app']
        api = create_blueprint_api(app, 'api_plugin', __name__)
        api.add_resource(OpenAPIResource, '/api/api.yml')
