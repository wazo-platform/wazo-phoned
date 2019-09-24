# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .resource import Status


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        api.add_resource(Status, '/status')
