# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from flask import request, current_app
from requests.exceptions import RequestException

from wazo_phoned.plugin_helpers.proxy.resource import (
    _build_next_url,
    _error,
    _response_dird,
    DIRD_API_VERSION,
    ProxyLookup,
)

from .schema import LookupGigasetSchema


class Lookup(ProxyLookup):
    def get(self, profile, xivo_user_uuid):
        args = LookupGigasetSchema().load(request.args)
        offset = args['first'] - 1
        limit = args['limit']
        term = args['term'].replace('*', '') if args['term'] else ''

        url = 'https://{host}:{port}/{version}/directories/lookup/{profile}/{xivo_user_uuid}/gigaset'
        params = {'term': term, 'limit': limit, 'offset': offset}

        try:
            headers = {
                'X-Auth-Token': current_app.config.get('token'),
                'Proxy-URL': _build_next_url('lookup'),
                'Accept-Language': request.headers.get('Accept-Language'),
            }
            return _response_dird(
                url.format(
                    host=self.dird_host,
                    port=self.dird_port,
                    version=DIRD_API_VERSION,
                    profile=profile,
                    xivo_user_uuid=xivo_user_uuid,
                ),
                headers=headers,
                params=params,
                verify=self.dird_verify_certificate,
            )
        except RequestException as e:
            return _error(e.code, str(e))
