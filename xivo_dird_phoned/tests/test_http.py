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

from hamcrest import assert_that, equal_to
from unittest import TestCase

from xivo_dird_phoned import http


class TestHTTP(TestCase):

    def test_that_find_vendor_by_user_agent_return_vendor_cisco(self):
        expected_result = 'cisco'
        user_agent_1 = 'xxx-Allegro-alice-12356'
        user_agent_2 = 'xxx-Cisco-alice-12356'
        result_1 = http._find_vendor_by_user_agent(user_agent_1)
        result_2 = http._find_vendor_by_user_agent(user_agent_2)

        assert_that(result_1, equal_to(expected_result))
        assert_that(result_2, equal_to(expected_result))

    def test_that_find_vendor_by_user_agent_return_vendor_aastra(self):
        expected_result = 'aastra'
        user_agent = 'xxx-Aastra-alice-12356'
        result = http._find_vendor_by_user_agent(user_agent)

        assert_that(result, equal_to(expected_result))

    def test_that_find_vendor_by_user_agent_return_vendor_polycom(self):
        expected_result = 'polycom'
        user_agent = 'xxx-Polycom-webBrowser-12356'
        result = http._find_vendor_by_user_agent(user_agent)

        assert_that(result, equal_to(expected_result))

    def test_that_find_vendor_by_user_agent_return_vendor_snom(self):
        expected_result = 'snom'
        user_agent = 'xxx-Snom-alice-12356'
        result = http._find_vendor_by_user_agent(user_agent)

        assert_that(result, equal_to(expected_result))

    def test_that_find_vendor_by_user_agent_return_vendor_thomson(self):
        expected_result = 'thomson'
        user_agent = 'xxx-THOMSON-alice-12356'
        result = http._find_vendor_by_user_agent(user_agent)

        assert_that(result, equal_to(expected_result))

    def test_that_find_vendor_by_user_agent_return_vendor_yealink(self):
        expected_result = 'yealink'
        user_agent = 'xxx-yealink-alice-12356'
        result = http._find_vendor_by_user_agent(user_agent)

        assert_that(result, equal_to(expected_result))

    def test_that_find_vendor_by_user_agent_return_none_when_no_supported_user_agent(self):
        expected_result = None
        user_agent = 'xxx-not_supported-alice-12356'
        result = http._find_vendor_by_user_agent(user_agent)

        assert_that(result, equal_to(expected_result))
