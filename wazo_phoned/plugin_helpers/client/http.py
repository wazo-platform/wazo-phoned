# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import re

from collections import namedtuple
from flask import (
    render_template,
    request,
    Response,
)
from operator import attrgetter
from requests.exceptions import ConnectionError, HTTPError

from wazo_phoned.auth_remote_addr import AuthResource

from .exceptions import WazoAuthConnectionError, WazoDirdConnectionError, NoSuchUser
from .schema import UserUUIDSchema, LookupSchema
from ..common import output_error


logger = logging.getLogger(__name__)

_PhoneFormattedResult = namedtuple('_PhoneFormattedResult', ['name', 'number'])


class ClientMenu(AuthResource):

    content_type = None
    template = None

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('vendor')
        self.dird_client = kwargs.pop('dird_client')
        self.auth_client = kwargs.pop('auth_client')
        super().__init__(*args, **kwargs)

    def get(self, profile):
        args = UserUUIDSchema().load(request.args)
        xivo_user_uuid = args['xivo_user_uuid']

        response_rendered = render_template(
            self.template,
            xivo_user_uuid=xivo_user_uuid,
            xivo_proxy_url=_build_next_url('menu'),
        )

        return Response(response_rendered, content_type=self.content_type, status=200)


class ClientInput(AuthResource):

    content_type = None
    template = None

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('vendor')
        self.dird_client = kwargs.pop('dird_client')
        self.auth_client = kwargs.pop('auth_client')
        super().__init__(*args, **kwargs)

    def get(self, profile):
        args = UserUUIDSchema().load(request.args)
        xivo_user_uuid = args['xivo_user_uuid']

        response_rendered = render_template(
            self.template,
            xivo_user_uuid=xivo_user_uuid,
            xivo_proxy_url=_build_next_url('input'),
        )

        return Response(response_rendered, content_type=self.content_type, status=200)


class ClientLookup(AuthResource):

    MAX_ITEM_PER_PAGE = None
    content_type = None
    template = None

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('vendor')
        self.dird_client = kwargs.pop('dird_client')
        self.auth_client = kwargs.pop('auth_client')
        super().__init__(*args, **kwargs)

    def get(self, profile):
        args = LookupSchema().load(request.args)
        limit = args['limit'] if args['limit'] is not None else self.MAX_ITEM_PER_PAGE
        offset = args['offset']
        term = args['term']
        xivo_user_uuid = args['xivo_user_uuid']

        user_tenant = self._get_user_tenant_uuid(xivo_user_uuid)

        try:
            results_lookup = self.dird_client.directories.lookup_user(
                profile=profile,
                user_uuid=xivo_user_uuid,
                term=term,
                tenant_uuid=user_tenant,
            )
        except HTTPError as e:
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)
            reason = getattr(response, 'reason', str(e))
            return output_error(status_code, str(reason))
        except ConnectionError:
            raise WazoDirdConnectionError()

        logger.debug('Raw lookup results: %s', results_lookup)
        formatter = _PhoneResultFormatter(results_lookup)
        formatted_results = formatter.format_results()
        formatted_results.sort(key=attrgetter('name', 'number'))

        if limit is not None:
            paginated_results = formatted_results[offset : offset + limit]
        else:
            paginated_results = formatted_results[offset:]

        total_results = len(formatted_results)

        response_rendered = render_template(
            self.template,
            results=paginated_results,
            xivo_proxy_url=request.base_url,
            xivo_user_uuid=xivo_user_uuid,
            term=term,
            limit=limit,
            total=total_results,
            offset=offset,
            offset_next=self._next_offset(offset, limit, total_results),
            offset_previous=self._previous_offset(offset, limit),
        )

        return Response(response_rendered, content_type=self.content_type, status=200)

    def _next_offset(self, offset, limit, results_count):
        if limit is None:
            return None

        next_offset = offset + limit
        if next_offset >= results_count:
            return None

        return next_offset

    def _previous_offset(self, offset, limit):
        if offset == 0:
            return None

        if limit is None:
            return None

        previous_offset = offset - limit
        if previous_offset < 0:
            return 0

        return previous_offset

    def _get_user_tenant_uuid(self, user_uuid):
        try:
            return self.auth_client.users.get(user_uuid)['tenant_uuid']
        except HTTPError as e:
            response = getattr(e, 'response', None)
            status_code = getattr(response, 'status_code', None)
            if status_code == 404:
                raise NoSuchUser(user_uuid)
            raise
        except ConnectionError:
            raise WazoAuthConnectionError()


def _build_next_url(current):
    if current == 'menu':
        return request.base_url.replace('menu', 'input', 1)
    if current == 'input':
        return request.base_url.replace('input', 'lookup', 1)
    if current == 'lookup':
        return request.base_url
    return None


class _PhoneResultFormatter:

    _NAME_FIELD = 'name'
    _NUMBER_FIELD = 'number'
    _INVALID_CHARACTERS_REGEX = re.compile(r'[^\d*#+\(\)]+')
    _SPECIAL_NUMBER_REGEX = re.compile(r'^\+(\d+)\(\d+\)(\d+)$')
    _PARENTHESES_REGEX = re.compile(r'[\(\)]')

    def __init__(self, lookup_results):
        self._lookup_results = lookup_results
        self._number_fields = self._extract_number_fields()
        self._name_field_position = self._find_name_field_position()

    def format_results(self):
        results = []
        for lookup_result in self._lookup_results['results']:
            self._format_result(lookup_result, results)
        return results

    def _format_result(self, result, out):
        for display_name, number in self._extract_result(result):
            number = self._normalize_number(number)
            if not number:
                continue
            out.append(_PhoneFormattedResult(display_name, number))

    def _normalize_number(self, number):
        number = self._extract_number_from_pretty_number(number)
        return number

    def _extract_result(self, result):
        name = result['column_values'][self._name_field_position]
        first_number = True
        for candidate in self._number_fields:
            if first_number:
                name_result = name
            else:
                name_result = '{} ({})'.format(
                    name, self._lookup_results['column_headers'][candidate].lower()
                )
            number = result['column_values'][candidate]
            if not number:
                continue
            yield name_result, number
            first_number = False

    def _extract_number_from_pretty_number(self, pretty_number):
        number_with_parentheses = self._INVALID_CHARACTERS_REGEX.sub('', pretty_number)
        # Convert numbers +33(0)123456789 to 0033123456789
        number_with_parentheses = self._SPECIAL_NUMBER_REGEX.sub(
            r'00\1\2', number_with_parentheses
        )
        return self._PARENTHESES_REGEX.sub('', number_with_parentheses)

    def _extract_number_fields(self):
        return [
            position
            for position, field in enumerate(self._lookup_results['column_types'])
            if field == self._NUMBER_FIELD
        ]

    def _find_name_field_position(self):
        return self._lookup_results['column_types'].index(self._NAME_FIELD)
