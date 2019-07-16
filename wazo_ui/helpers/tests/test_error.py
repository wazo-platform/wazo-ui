# Copyright 2018 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from hamcrest import assert_that, equal_to, is_, none
from mock import Mock

from ..error import ErrorExtractor, ErrorTranslator

GENERIC_MESSAGE_ERRORS = {'resource-not-found': 'Resource not found',
                          'invalid-data': 'Input error'}

SPECIFIC_MESSAGE_ERRORS = {'required': 'Missing data for required field',
                           'invalid-choice': 'Not a valid choice'}

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
