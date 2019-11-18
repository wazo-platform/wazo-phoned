# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, equal_to, has_items
from unittest import TestCase
from mock import patch

from .. import http


class TestHTTP(TestCase):
    @patch('wazo_phoned.plugin_helpers.client.http.request')
    def test_that_build_next_url_return_input_url_when_is_menu(self, MockedRequest):
        current_url = 'http://127.0.0.1:9498/0.1/directories/{}/profile/vendor'
        expected_result = current_url.format('input')
        MockedRequest.base_url = current_url.format('menu')
        result = http._build_next_url('menu')

        assert_that(result, equal_to(expected_result))

    @patch('wazo_phoned.plugin_helpers.client.http.request')
    def test_that_build_next_url_return_input_url_when_is_menu_with_profile_menu(
        self, MockedRequest
    ):
        current_url = 'http://127.0.0.1:9498/0.1/directories/{}/menu/vendor'
        expected_result = current_url.format('input')
        MockedRequest.base_url = current_url.format('menu')
        result = http._build_next_url('menu')

        assert_that(result, equal_to(expected_result))

    @patch('wazo_phoned.plugin_helpers.client.http.request')
    def test_that_build_next_url_return_lookup_url_when_is_input(self, MockedRequest):
        current_url = 'http://127.0.0.1:9498/0.1/directories/{}/profile/vendor'
        expected_result = current_url.format('lookup')
        MockedRequest.base_url = current_url.format('input')
        result = http._build_next_url('input')

        assert_that(result, equal_to(expected_result))

    @patch('wazo_phoned.plugin_helpers.client.http.request')
    def test_that_build_next_url_return_lookup_url_when_is_input_with_profile_input(
        self, MockedRequest
    ):
        current_url = 'http://127.0.0.1:9498/0.1/directories/{}/input/vendor'
        expected_result = current_url.format('lookup')
        MockedRequest.base_url = current_url.format('input')
        result = http._build_next_url('input')

        assert_that(result, equal_to(expected_result))

    @patch('wazo_phoned.plugin_helpers.client.http.request')
    def test_that_build_next_url_return_same_url_when_is_lookup(self, MockedRequest):
        current_url = 'http://127.0.0.1:9498/0.1/directories/lookup/profile/vendor'
        expected_result = current_url
        MockedRequest.base_url = current_url
        result = http._build_next_url('lookup')

        assert_that(result, equal_to(expected_result))

    def test_that_next_offset_when_no_limit_is_none(self):
        result = http._next_offset(offset=2, limit=None, results_count=10)
        assert_that(result, equal_to(None))

    def test_that_next_offset_is_current_offset_when_limit_is_zero(self):
        result = http._next_offset(offset=2, limit=0, results_count=10)
        assert_that(result, equal_to(2))

    def test_that_next_offset_is_none_when_offset_bigger_than_results(self):
        result = http._next_offset(offset=20, limit=1, results_count=10)
        assert_that(result, equal_to(None))

    def test_that_next_offset_returns_right_number_when_inferior_to_max(self):
        result = http._next_offset(offset=0, limit=5, results_count=10)
        assert_that(result, equal_to(5))

    def test_that_next_offset_returns_none_when_offset_plus_limit_superior_to_max(self):
        result = http._next_offset(offset=15, limit=10, results_count=20)
        assert_that(result, equal_to(None))

    def test_that_previous_offset_when_no_limit_is_none(self):
        result = http._previous_offset(offset=2, limit=None)
        assert_that(result, equal_to(None))

    def test_that_previous_offset_is_none_when_offset_zero(self):
        result = http._previous_offset(offset=0, limit=10)
        assert_that(result, equal_to(None))

    def test_that_previous_offset_is_zero_when_limit_larger_than_offset(self):
        result = http._previous_offset(offset=5, limit=10)
        assert_that(result, equal_to(0))

    def test_that_previous_offset_is_previous_number_when_limit_is_one(self):
        result = http._previous_offset(offset=5, limit=1)
        assert_that(result, equal_to(4))

    def test_that_previous_offset_is_zero_when_offset_and_limit_equals(self):
        result = http._previous_offset(offset=5, limit=5)
        assert_that(result, equal_to(0))


class TestPhoneResultFormatter(TestCase):
    def setUp(self):
        self.lookup_results = {
            'column_headers': ['h1', 'h2', 'h3', 'h4'],
            'column_types': ['name', 'number', 'number', 'number'],
            'results': [{'column_values': ['R1', '1234', '56789', '0000']}],
        }
        self.formatter = http._PhoneResultFormatter(self.lookup_results)

    def test_extract_number_from_pretty_european_number_is_valid(self):
        pretty_number = '+33(0)123456789'
        expected_number = '0033123456789'
        result = self.formatter._extract_number_from_pretty_number(pretty_number)
        assert_that(result, equal_to(expected_number))

    def test_extract_number_from_pretty_american_number_is_valid(self):
        pretty_number = '(555)555-5555'
        expected_number = '5555555555'
        result = self.formatter._extract_number_from_pretty_number(pretty_number)
        assert_that(result, equal_to(expected_number))

    def test_result_numbers_have_column_header_suffix(self):
        result_numbers = list(
            self.formatter._extract_result(self.lookup_results['results'][0])
        )
        assert_that(
            result_numbers,
            has_items(('R1', '1234'), ('R1 (h3)', '56789'), ('R1 (h4)', '0000')),
        )
