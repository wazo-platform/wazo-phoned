# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.flask.metrics import init_flask_metrics

from wazo_phoned.auth import verify_remote_addr


class Plugin:
    def load(self, dependencies):
        # phoned listens on 0.0.0.0 without nginx: only authorized subnets
        init_flask_metrics(dependencies['api'], metrics_decorator=verify_remote_addr)
