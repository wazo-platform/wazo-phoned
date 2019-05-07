# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, equal_to
from unittest import TestCase
from mock import patch

from .. import http


class TestHTTP(TestCase):

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
