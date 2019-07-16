# Copyright 2018 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from flask import Flask
from hamcrest import assert_that, empty, is_, equal_to, has_items, matches_regexp
from mock import Mock
from wtforms import StringField

from ..classful import BaseView, _is_positive_integer, extract_select2_params, build_select2_response
from ..error import ErrorExtractor, ErrorTranslator
from ..form import BaseForm

URL_TO_NAME_RESOURCES = {'resources_url': 'resource'}

GENERIC_MESSAGE_ERRORS = {'invalid-data': 'Input Error'}

SPECIFIC_MESSAGE_ERRORS = {
    'invalid-length': 'Longer than maximum length',
    'invalid-length2': 'Longer than maximum length2'
}

app = Flask('test_wazo_ui')


class TestBaseView(unittest.TestCase):

    def setUp(self):
        self.view = BaseView()
        ErrorExtractor.url_to_name_resources = URL_TO_NAME_RESOURCES
        ErrorTranslator.generic_messages = GENERIC_MESSAGE_ERRORS
        ErrorTranslator.specific_messages = SPECIFIC_MESSAGE_ERRORS
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        class MyForm(BaseForm):
            attribute1 = StringField()

        with app.test_request_context(method='POST', data={'attribute1': ''}):
            self.form = MyForm()

    def test_fill_form_error_with_input_error(self):
        error = {
            'message': 'Sent data is invalid',
            'details': {
                'attribute1': {
                    'message': 'Longer than maximum length',
                    'constraint': {'max': 128, 'min': 1},
                    'constraint_id': 'invalid-length'
                }
            },
            'error_id': 'invalid-data'
        }
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(error, path_url))

        assert_that(form.attribute1.errors, has_items(
            matches_regexp(r'Longer than maximum length \(\{\'[min|max]+\': [0-9]+, \'[min|max]+\': [0-9]+\}\)'),
        ))

    def test_fill_form_error_with_list_input_error(self):
        error = {
            'message': 'Sent data is invalid',
            'details': {
                'attribute1': [
                    {
                        'message': 'Longer than maximum length',
                        'constraint': {'max': 128, 'min': 1},
                        'constraint_id': 'invalid-length'
                    }
                ]
            },
            'error_id': 'invalid-data'
        }
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(error, path_url))

        assert_that(form.attribute1.errors, has_items(
            matches_regexp(r'Longer than maximum length \(\{\'[min|max]+\': [0-9]+, \'[min|max]+\': [0-9]+\}\)'),
        ))

    def test_fill_form_error_with_multiple_input_error(self):
        error = {
            'message': 'Sent data is invalid',
            'details': {
                'attribute1': [
                    {
                        'message': 'Longer than maximum length',
                        'constraint': {'max': 128, 'min': 1},
                        'constraint_id': 'invalid-length'
                    },
                    {
                        'message': 'Longer than maximum length2',
                        'constraint': {'max': 8, 'min': 5},
                        'constraint_id': 'invalid-length2'
                    }
                ]
            },
            'error_id': 'invalid-data'
        }
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(error, path_url))

        assert_that(form.attribute1.errors, has_items(
            matches_regexp(r'Longer than maximum length \(\{\'[min|max]+\': [0-9]+, \'[min|max]+\': [0-9]+\}\)'),
            matches_regexp(r'Longer than maximum length2 \(\{\'[min|max]+\': [0-9]+, \'[min|max]+\': [0-9]+\}\)')
        ))

    def test_fill_form_error_with_input_error_and_not_constraint(self):
        error = {
            'message': 'Sent data is invalid',
            'details': {
                'attribute1': {'message': 'Unregistered message'}
            },
            'error_id': 'invalid-data'
        }
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(error, path_url))

        assert_that(form.attribute1.errors, None)

    def test_fill_form_error_with_input_error_and_invalid_attribute(self):
        error = {
            'message': 'Sent data is invalid',
            'details': {
                'invalid_attr': {'message': 'Longer than maximum length'}
            },
            'error_id': 'invalid-data'
        }
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_input_error_and_invalid_format(self):
        error = {
            'message': 'User was not found ("uuid": "patate")',
            'details': {},
            'error_id': 'invalid-data'
        }
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_not_input_error(self):
        error = {
            'message': 'Some Error',
            'details': {},
            'error_id': 'invalid-data'
        }
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(error, path_url))

        assert_that(form.attribute1.errors, empty())

    def _build_error(self, error, path_url):
        return Mock(response=Mock(json=Mock(return_value=error)),
                    request=Mock(path_url=path_url))


class TestSelect2Helpers(unittest.TestCase):

    def test_is_positive_integer(self):
        response = _is_positive_integer(1)
        assert_that(response, is_(True))

    def test_is_positive_integer_when_string_integer(self):
        response = _is_positive_integer('1')
        assert_that(response, is_(True))

    def test_is_positive_integer_when_none(self):
        response = _is_positive_integer(None)
        assert_that(response, is_(False))

    def test_is_positive_integer_when_negative(self):
        response = _is_positive_integer(-1)
        assert_that(response, is_(False))

    def test_is_positive_integer_when_string(self):
        response = _is_positive_integer('abcd')
        assert_that(response, is_(False))

    def test_extract_select2_params(self):
        args = {'term': 'a', 'page': 1}
        result = extract_select2_params(args, limit=10)
        assert_that(result, equal_to({'search': 'a',
                                      'offset': 0,
                                      'limit': 10}))

    def test_extract_select2_params_when_no_args(self):
        args = {}
        result = extract_select2_params(args, limit=10)
        assert_that(result, equal_to({'search': None,
                                      'offset': 0,
                                      'limit': 10}))

    def test_extract_select2_params_when_page_is_not_positive_integer(self):
        args = {'page': 'abcd'}
        result = extract_select2_params(args, limit=10)
        assert_that(result, equal_to({'search': None,
                                      'offset': 0,
                                      'limit': 10}))

    def test_extract_select2_params_when_page_is_more_than_one(self):
        args = {'page': 3}
        result = extract_select2_params(args, limit=10)
        assert_that(result, equal_to({'search': None,
                                      'offset': 20,
                                      'limit': 10}))

    def test_build_select2_response_with_pagination(self):
        result = [{'key': 'value'}]
        total = 42
        params = {'search': 'a', 'offset': 10, 'limit': 10}
        response = build_select2_response(result, total, params)
        assert_that(response, equal_to({'results': result,
                                        'pagination': {'more': True}}))

    def test_build_select2_response_without_pagination(self):
        result = [{'key': 'value'}]
        total = 15
        params = {'search': 'a', 'offset': 10, 'limit': 10}
        response = build_select2_response(result, total, params)
        assert_that(response, equal_to({'results': result,
                                        'pagination': {'more': False}}))
