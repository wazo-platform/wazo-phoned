# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging

from flask import current_app
from flask import request
from flask_restful import Resource
from flask_restful import abort
from functools import wraps
from netaddr import IPNetwork, IPAddress

logger = logging.getLogger(__name__)


def verify_remote_addr(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        remote_addr = request.remote_addr
        if not remote_addr:
            abort(401)

        networks = current_app.config['hosts_authorized']
        for network in networks:
            if IPAddress(remote_addr) in IPNetwork(network):
                return func(*args, **kwargs)

        abort(401)
    return wrapper


class AuthResource(Resource):
    method_decorators = [verify_remote_addr]
