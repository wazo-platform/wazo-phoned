# Copyright 2020-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_confd_client import Client as ConfdClient

from wazo_phoned.plugin_helpers.common import create_blueprint_api

from .http import (
    EndpointAnswerResource,
    EndpointHoldStartResource,
    EndpointHoldStopResource,
)
from .services import EndpointService


class Plugin:
    def load(self, dependencies):
        app = dependencies['app']
        api = create_blueprint_api(app, 'endpoints', __name__)
        confd_client = ConfdClient(**dependencies['config']['confd'])
        token_changed_subscribe = dependencies['token_changed_subscribe']
        token_changed_subscribe(confd_client.set_token)

        service = EndpointService(dependencies['phone_plugins'], confd_client)
        class_kwargs = {
            'service': service,
        }
        api.add_resource(
            EndpointHoldStartResource,
            '/endpoints/<endpoint_name>/hold/start',
            endpoint='endpoint_hold_start',
            resource_class_kwargs=class_kwargs,
        )
        api.add_resource(
            EndpointHoldStopResource,
            '/endpoints/<endpoint_name>/hold/stop',
            endpoint='endpoint_hold_stop',
            resource_class_kwargs=class_kwargs,
        )
        api.add_resource(
            EndpointAnswerResource,
            '/endpoints/<endpoint_name>/answer',
            endpoint='endpoint_answer',
            resource_class_kwargs=class_kwargs,
        )
