# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.mallow import fields
from xivo.mallow_helpers import Schema


class UserUUIDSchema(Schema):
    xivo_user_uuid = fields.String(required=True)


class LookupSchema(UserUUIDSchema):
    term = fields.String(required=True)
    limit = fields.Integer(missing=None)
    offset = fields.Integer(missing=0)


class UserServiceSchema(Schema):
    user_uuid = fields.String(required=True)
    enabled = fields.Boolean(missing=None)
