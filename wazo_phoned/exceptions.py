# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from xivo import rest_api_helpers

logger = logging.getLogger(__name__)


APIException = rest_api_helpers.APIException


class MasterTenantNotInitialized(APIException):
    def __init__(self):
        msg = 'wazo-phoned master tenant is not initialized'
        super().__init__(503, msg, 'master-tenant-not-initialized')
