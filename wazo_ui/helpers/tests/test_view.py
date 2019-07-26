# Copyright 2018 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from flask import Flask
from hamcrest import assert_that, contains, empty
from mock import Mock
from wtforms import StringField

from wazo_ui.helpers.form import BaseForm

from ..error import ConfdErrorExtractor, ErrorTranslator
from ..view import BaseIPBXHelperView

URL_TO_NAME_RESOURCES = {'resources_url': 'resource'}

GENERIC_PATTERN_ERRORS = {'invalid-data': r'^Input Error'}
GENERIC_MESSAGE_ERRORS = {'invalid-data': 'Input Error'}

SPECIFIC_PATTERN_ERRORS = {'invalid-length': r'Longer than maximum length'}
SPECIFIC_MESSAGE_ERRORS = {'invalid-length': 'Longer than maximum length'}

app = Flask('test_nestbox_ui')


class TestBaseView(unittest.TestCase):

    def setUp(self):
        self.view = BaseIPBXHelperView()
        ConfdErrorExtractor.generic_patterns = GENERIC_PATTERN_ERRORS
        ConfdErrorExtractor.specific_patterns = SPECIFIC_PATTERN_ERRORS
        ConfdErrorExtractor.url_to_name_resources = URL_TO_NAME_RESOURCES
        ErrorTranslator.generic_messages = GENERIC_MESSAGE_ERRORS
        ErrorTranslator.specific_messages = SPECIFIC_MESSAGE_ERRORS
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        class MyForm(BaseForm):
            attribute1 = StringField()

        with app.test_request_context(method='POST', data={'attribute1': ''}):
            self.form = MyForm()

    def test_fill_form_error_with_confd_input_error(self):
        confd_error = ["Input Error - attribute1: 'Longer than maximum length'"]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, contains('Longer than maximum length'))

    def test_fill_form_error_with_confd_input_error_and_not_register_msg(self):
        confd_error = ["Input Error - attribute1: 'Unregistered message'"]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_input_error_and_invalid_attribute(self):
        confd_error = ["Input Error - invalid_attr: 'Longer than maximum length'"]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_input_error_and_invalid_format(self):
        confd_error = ["Input Error - field 'users': User was not found ('uuid': 'patate')"]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def test_fill_form_error_with_confd_not_input_error(self):
        confd_error = ["Some Error - "]
        path_url = '/1.1/resources_url/42'
        form = self.view._fill_form_error(self.form, self._build_error(confd_error, path_url))

        assert_that(form.attribute1.errors, empty())

    def _build_error(self, error, path_url):
        return Mock(response=Mock(json=Mock(return_value=error)),
                    request=Mock(path_url=path_url))
