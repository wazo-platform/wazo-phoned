# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.mallow import fields
from xivo.mallow_helpers import Schema


class LookupGigasetSchema(Schema):
    set_first = fields.String(attribute='term', missing='')
    count = fields.Integer(attribute='limit', missing=None)
    first = fields.Integer(attribute='first', missing=1)
