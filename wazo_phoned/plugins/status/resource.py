# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import current_app

from wazo_phoned.auth_remote_addr import AuthResource


class Status(AuthResource):
    def get(self):
        return {
            'service_token': {
                'status': 'ok' if current_app.config.get('token') else 'fail'
            }
        }
