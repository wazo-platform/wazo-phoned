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

import time

from hamcrest import assert_that
from hamcrest import contains_string

from .base_dird_phoned_integration_test import BaseDirdPhonedIntegrationTest


class TestHTTPSMissingCertificate(BaseDirdPhonedIntegrationTest):
    asset = 'no_authentication'

    def test_given_inexisting_authentication_when_dird_phoned_starts_then_dird_phoned_stops(self):
        for _ in range(5):
            status = self.dird_phoned_status()[0]
            if not status['State']['Running']:
                break
            time.sleep(1)
        else:
            self.fail('xivo-dird-phoned did not stop while missing authentication')

        log = self.dird_phoned_logs()
        assert_that(log, contains_string("No such file or directory: '/etc/xivo-dird-phoned/authentication.yml'"))
