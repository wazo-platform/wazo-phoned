# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo.mallow import fields
from xivo.mallow_helpers import Schema


class LookupGigasetSchema(Schema):
    set_first = fields.String(attribute='term', load_default='')
    count = fields.Integer(attribute='limit', load_default=None)
    first = fields.Integer(attribute='offset', load_default=1)
