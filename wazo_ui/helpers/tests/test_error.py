# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import Mock

from hamcrest import any_of, assert_that, empty, equal_to, is_, none

from ..error import (
    ConfdErrorExtractor,
    ConfdErrorTranslator,
    ErrorExtractor,
    ErrorTranslator,
)

GENERIC_MESSAGE_ERRORS = {
    'resource-not-found': 'Resource not found',
    'invalid-data': 'Input error',
}

SPECIFIC_MESSAGE_ERRORS = {
    'required': 'Missing data for required field',
    'invalid-choice': 'Not a valid choice',
}

URL_TO_NAME_RESOURCES = {'resource_url': 'resource'}


class TestErrorTranslator(unittest.TestCase):
    def setUp(self):
        ErrorTranslator.register_generic_messages(GENERIC_MESSAGE_ERRORS)
        ErrorTranslator.register_specific_messages(SPECIFIC_MESSAGE_ERRORS)

    def test_translate_constraint(self):
        constraint = 'required'
        field_message = ErrorTranslator.translate_constraint(constraint)
        assert_that(field_message, equal_to('Missing data for required field'))

    def test_translate_constraint_when_does_not_match(self):
        constraint = 'constraint_not_exist'
        field_message = ErrorTranslator.translate_constraint(constraint)
        assert_that(field_message, equal_to(constraint))


class TestErrorExtractor(unittest.TestCase):
    def setUp(self):
        ErrorExtractor.register_url_to_name_resources(URL_TO_NAME_RESOURCES)

    def test_extract_resource_when_does_not_match(self):
        request = Mock(path_url='/1.1/resource/too/long')
        resource = ErrorExtractor.extract_resource(request)
        assert_that(resource, is_(none()))

    def test_extract_resource(self):
        request = Mock(path_url='/1.1/resource')
        resource = ErrorExtractor.extract_resource(request)
        assert_that(resource, equal_to('resource'))

    def test_extract_resource_with_id(self):
        request = Mock(path_url='/1.1/resource/id')
        resource = ErrorExtractor.extract_resource(request)
        assert_that(resource, equal_to('resource'))

    def test_extract_resource_when_match_on_url_resource(self):
        request = Mock(path_url='/1.1/resource_url/id')
        resource = ErrorExtractor.extract_resource(request)
        assert_that(resource, equal_to('resource'))


GENERIC_PATTERN_ERRORS = {
    'resource-not-found': r'^Resource Not Found',
    'invalid-data': r'^Input Error',
}

GENERIC_MESSAGE_ERRORS = {
    'resource-not-found': 'Resource not found',
    'invalid-data': 'Input error',
}

SPECIFIC_PATTERN_ERRORS = {
    'required': r'Missing data for required field',
    'invalid-choice': r'Not a valid choice',
}

SPECIFIC_MESSAGE_ERRORS = {
    'required': 'Missing data for required field',
    'invalid-choice': 'Not a valid choice',
}

URL_TO_NAME_RESOURCES = {'resource_url': 'resource'}


class TestConfdErrorTranslator(unittest.TestCase):
    def setUp(self):
        ConfdErrorTranslator.register_generic_messages(GENERIC_MESSAGE_ERRORS)
        ConfdErrorTranslator.register_specific_messages(SPECIFIC_MESSAGE_ERRORS)

    def test_translate_specific_error_id_from_fields(self):
        fields = {'name': 'required', 'description': 'invalid-choice'}
        field_message = ConfdErrorTranslator.translate_specific_error_id_from_fields(
            fields
        )
        expected = {
            'name': 'Missing data for required field',
            'description': 'Not a valid choice',
        }
        assert_that(field_message, equal_to(expected))

    def test_translate_specific_error_id_from_fields_when_dict(self):
        fields = {'name': {'patate': 'required', 'pomme': 'invalid-choice'}}
        field_message = ConfdErrorTranslator.translate_specific_error_id_from_fields(
            fields
        )
        expected = {
            'name': {
                'patate': 'Missing data for required field',
                'pomme': 'Not a valid choice',
            }
        }
        assert_that(field_message, equal_to(expected))


class TestConfdErrorExtractor(unittest.TestCase):
    def setUp(self):
        ConfdErrorExtractor.register_generic_patterns(GENERIC_PATTERN_ERRORS)
        ConfdErrorExtractor.register_specific_patterns(SPECIFIC_PATTERN_ERRORS)

    def test_extract_specific_error_id_from_fields(self):
        fields = {
            'name': ['Missing data for required field'],
            'description': ['Not a valid choice'],
        }
        error_ids = ConfdErrorExtractor.extract_specific_error_id_from_fields(fields)

        expected = {'name': 'required', 'description': 'invalid-choice'}
        assert_that(error_ids, equal_to(expected))

    def test_extract_specific_error_id_from_fields_when_string(self):
        fields = {'name': 'Missing data for required field'}
        error_ids = ConfdErrorExtractor.extract_specific_error_id_from_fields(fields)

        expected = {'name': 'required'}
        assert_that(error_ids, equal_to(expected))

    def test_extract_specific_error_id_from_fields_when_embeded_fields(self):
        fields = {
            '1': {
                'name': ['Missing data for required field'],
                'description': ['Not a valid choice'],
            }
        }
        error_ids = ConfdErrorExtractor.extract_specific_error_id_from_fields(fields)

        expected = {'1': {'name': 'required', 'description': 'invalid-choice'}}
        assert_that(error_ids, equal_to(expected))

    def test_extract_specific_error_id_from_fields_when_field_with_multiple_errors(
        self,
    ):
        fields = {'name': ['Missing data for required field' 'Not a valid choice']}
        error_ids = ConfdErrorExtractor.extract_specific_error_id_from_fields(fields)

        expected1 = {'name': 'required'}
        expected2 = {'name': 'invalid-choice'}
        assert_that(error_ids, any_of(expected1, expected2))

    def test_extract_specific_error_id_from_fields_when_fields_empty(self):
        fields = {}
        error_ids = ConfdErrorExtractor.extract_specific_error_id_from_fields(fields)
        assert_that(error_ids, empty())

    def test_extract_specific_error_id_from_fields_when_field_not_match(self):
        fields = {'name': 'unregister pattern'}
        error_ids = ConfdErrorExtractor.extract_specific_error_id_from_fields(fields)
        assert_that(error_ids, empty())

    def test_extract_specific_error_id_from_fields_when_field_with_object(self):
        fields = {'name': [{'key': 'Missing data for required field'}]}
        error_ids = ConfdErrorExtractor.extract_specific_error_id_from_fields(fields)

        expected = {'name': 'required'}
        assert_that(error_ids, equal_to(expected))

    def test_extract_generic_error_id_when_response_is_string(self):
        response = 'ERROR'
        error_id = ConfdErrorExtractor.extract_generic_error_id(response)
        assert_that(error_id, is_(none()))

    def test_extract_generic_error_id_when_response_is_list_with_match_error(self):
        response = ['Resource Not Found']
        error_id = ConfdErrorExtractor.extract_generic_error_id(response)
        assert_that(error_id, equal_to('resource-not-found'))

    def test_extract_generic_error_id_when_response_is_list_with_many_match_error(self):
        response = ['Resource Not Found', 'Input Error']
        error_id = ConfdErrorExtractor.extract_generic_error_id(response)
        assert_that(error_id, any_of('resource-not-found', 'invalid-data'))

    def test_extract_generic_error_id_when_response_is_list_with_no_match_error(self):
        response = ['Unregistered error']
        error_id = ConfdErrorExtractor.extract_generic_error_id(response)
        assert_that(error_id, is_(none()))

    def test_extract_field_when_message_does_not_match(self):
        message = 'Unregistered specific error'
        field = ConfdErrorExtractor.extract_field(message)
        assert_that(field, empty())

    def test_extract_field_when_message_is_simple(self):
        message = "Input Error - name: ['string does not match']"
        field = ConfdErrorExtractor.extract_field(message)

        expected = {'name': ['string does not match']}
        assert_that(field, equal_to(expected))

    def test_extract_field_when_message_is_complexe(self):
        message = "Input Error - funckeys: {'1': {'name': ['string error']}, \
                                            '2': {'label': ['label error']}}"
        field = ConfdErrorExtractor.extract_field(message)

        expected = {
            'funckeys': {
                '1': {'name': ['string error']},
                '2': {'label': ['label error']},
            }
        }
        assert_that(field, equal_to(expected))

    def test_extract_field_when_message_is_invalid_object(self):
        message = 'Input Error - name: {{invalid python object'
        field = ConfdErrorExtractor.extract_field(message)

        expected = {'name': '{{invalid python object'}
        assert_that(field, equal_to(expected))

    def test_extract_fields_when_response_is_empty(self):
        response = []
        fields = ConfdErrorExtractor.extract_fields(response)
        assert_that(fields, empty())

    def test_extract_fields_when_response_is_not_empty(self):
        message1 = "Input Error - name: ['name error1']"
        message2 = "Input Error - description: ['description error2']"
        response = [message1, message2]
        fields = ConfdErrorExtractor.extract_fields(response)

        expected = {'name': ['name error1'], 'description': ['description error2']}
        assert_that(fields, expected)

    def test_extract_fields_when_response_has_same_key(self):
        message1 = "Input Error - name: ['name error1']"
        message2 = "Input Error - name: ['name error2']"
        response = [message1, message2]
        fields = ConfdErrorExtractor.extract_fields(response)

        expected = {'name': ['name error2']}
        assert_that(fields, expected)
