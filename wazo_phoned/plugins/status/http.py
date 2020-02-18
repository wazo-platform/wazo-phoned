# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.auth_remote_addr import AuthResource


class Status(AuthResource):
    def __init__(self, status_aggregator):
        self.status_aggregator = status_aggregator

    def get(self):
        return self.status_aggregator.status(), 200
