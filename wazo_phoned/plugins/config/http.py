# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import request
from wazo_phoned.auth import TokenAuthResource
from xivo.auth_verifier import required_acl
from jsonpatch import JsonPatch

from wazo_phoned.auth import required_master_tenant

from .schemas import config_patch_schema


class ConfigResource(TokenAuthResource):
    def __init__(self, config_service):
        self._config_service = config_service

    @required_master_tenant()
    @required_acl('phoned.config.read')
    def get(self):
        return self._config_service.get_config(), 200

    @required_master_tenant()
    @required_acl('phoned.config.update')
    def patch(self):
        config_patch = config_patch_schema.load(request.get_json(), many=True)
        config = self._config_service.get_config()
        patched_config = JsonPatch(config_patch).apply(config)
        self._config_service.update_config(patched_config)
        return self._config_service.get_config(), 200
