# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that, equal_to
from unittest import TestCase
from mock import patch

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

    @patch('xivo_dird_phoned.http.request')
    def test_that_build_next_url_return_input_url_when_is_menu(self, MockedRequest):
        current_url = 'http://127.0.0.1:9498/0.1/directories/{}/profile/vendor'
        expected_result = current_url.format('input')
        MockedRequest.base_url = current_url.format('menu')
        result = http._build_next_url('menu')

        assert_that(result, equal_to(expected_result))

    @patch('xivo_dird_phoned.http.request')
    def test_that_build_next_url_return_input_url_when_is_menu_with_profile_menu(self, MockedRequest):
        current_url = 'http://127.0.0.1:9498/0.1/directories/{}/menu/vendor'
        expected_result = current_url.format('input')
        MockedRequest.base_url = current_url.format('menu')
        result = http._build_next_url('menu')

        assert_that(result, equal_to(expected_result))

    @patch('xivo_dird_phoned.http.request')
    def test_that_build_next_url_return_lookup_url_when_is_input(self, MockedRequest):
        current_url = 'http://127.0.0.1:9498/0.1/directories/{}/profile/vendor'
        expected_result = current_url.format('lookup')
        MockedRequest.base_url = current_url.format('input')
        result = http._build_next_url('input')

        assert_that(result, equal_to(expected_result))

    @patch('xivo_dird_phoned.http.request')
    def test_that_build_next_url_return_lookup_url_when_is_input_with_profile_input(self, MockedRequest):
        current_url = 'http://127.0.0.1:9498/0.1/directories/{}/input/vendor'
        expected_result = current_url.format('lookup')
        MockedRequest.base_url = current_url.format('input')
        result = http._build_next_url('input')

        assert_that(result, equal_to(expected_result))

    @patch('xivo_dird_phoned.http.request')
    def test_that_build_next_url_return_same_url_when_is_lookup(self, MockedRequest):
        current_url = 'http://127.0.0.1:9498/0.1/directories/lookup/profile/vendor'
        expected_result = current_url
        MockedRequest.base_url = current_url
        result = http._build_next_url('lookup')

        assert_that(result, equal_to(expected_result))
