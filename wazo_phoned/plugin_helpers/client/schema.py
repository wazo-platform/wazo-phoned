# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from marshmallow import ValidationError, validates_schema
from xivo.mallow import fields
from xivo.mallow_helpers import Schema


class UserUUIDSchema(Schema):
    xivo_user_uuid = fields.String(required=True)


class LookupSchema(UserUUIDSchema):
    term = fields.String(required=True)
    limit = fields.Integer(missing=None)
    offset = fields.Integer(missing=0)


class UserForwardSchema(Schema):
    user_uuid = fields.String(required=True)
    destination = fields.String(missing=None)
    enabled = fields.Boolean(required=True)

    @validates_schema
    def validate_destination_when_enabled(seld, data, **kwargs):
        if data['enabled'] and not data['destination']:
            raise ValidationError({'destination': ['Destination must be set when enabling a service']})


class UserServiceSchema(Schema):
    user_uuid = fields.String(required=True)
    enabled = fields.Boolean(missing=None)
