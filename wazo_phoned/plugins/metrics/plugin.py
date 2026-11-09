# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import wraps

from flask import request
from netaddr import IPAddress
from xivo.flask.metrics import init_flask_metrics

from wazo_phoned.auth import verify_remote_addr


def verify_loopback_or_remote_addr(func):
    restricted = verify_remote_addr(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.remote_addr and IPAddress(request.remote_addr).is_loopback():
            return func(*args, **kwargs)
        return restricted(*args, **kwargs)

    return wrapper


class Plugin:
    def load(self, dependencies):
        # phoned listens on 0.0.0.0 without nginx: only local or authorized clients
        init_flask_metrics(
            dependencies['api'], metrics_decorator=verify_loopback_or_remote_addr
        )
