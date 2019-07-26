# Copyright 2018 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest

from flask import Flask
from hamcrest import assert_that, equal_to, empty, has_entries
from wtforms import StringField, FormField, IntegerField
from wtforms.fields import SelectField

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.destination import BaseDestinationForm, FallbacksForm


app = Flask('test_nestbox_ui')


class TemplateDestinationForm(BaseDestinationForm):
    select_field = 'template'

    template = SelectField()


class TestBaseDestinationForm(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        class UserForm(BaseForm):
            user_id = IntegerField()
            timeout = StringField()

        TemplateDestinationForm.user = FormField(UserForm)

    def test_to_dict(self):
        data = {'template': 'user',
                'user-user_id': 1,
                'user-timeout': '2'}

        with app.test_request_context(method='POST', data=data):
            form = TemplateDestinationForm()
        result = form.to_dict()

        assert_that(result, equal_to({'template': 'user',
                                      'user_id': 1,
                                      'timeout': '2'}))

    def test_to_dict_without_template(self):
        data = {}

        with app.test_request_context(method='POST', data=data):
            form = TemplateDestinationForm()
        result = form.to_dict()

        assert_that(result, empty())

    def test_to_dict_without_destination_values(self):
        data = {'template': 'none'}

        with app.test_request_context(method='POST', data=data):
            form = TemplateDestinationForm()
        result = form.to_dict()

        assert_that(result, equal_to({'template': 'none'}))

    def test_to_dict_with_empty_string(self):
        data = {'template': 'user',
                'user-user_id': 1,
                'user-timeout': ''}

        with app.test_request_context(method='POST', data=data):
            form = TemplateDestinationForm()
        result = form.to_dict()

        assert_that(result, equal_to({'template': 'user',
                                      'user_id': 1,
                                      'timeout': None}))

    def test_to_dict_without_select_field(self):
        data = {'template': 'none'}

        with app.test_request_context(method='POST', data=data):
            form = BaseDestinationForm()
        result = form.to_dict()

        assert_that(result, empty())

    def test_process(self):
        data = {'template': 'user',
                'user-user_id': 1,
                'user-timeout': '2'}

        with app.test_request_context(method='POST', data=data):
            form = TemplateDestinationForm()

        assert_that(form.data, has_entries(template='user',
                                           user={'user_id': 1,
                                                 'timeout': '2'}))

    def test_process_without_template(self):
        data = {}

        with app.test_request_context(method='POST', data=data):
            form = TemplateDestinationForm()

        assert_that(form.data, has_entries(template='None'))

    def test_process_with_kwargs(self):
        data = {'template': 'user',
                'user_id': 1,
                'timeout': '2'}

        with app.test_request_context():
            form = TemplateDestinationForm(**data)

        assert_that(form.data, has_entries(template='user',
                                           user={'user_id': 1,
                                                 'timeout': '2'}))

    def test_process_with_kwargs_and_undefined_form(self):
        data = {'template': 'queue',
                'queue_id': 1,
                'timeout': '2'}

        with app.test_request_context():
            form = TemplateDestinationForm(**data)

        assert_that(form.data, has_entries(template='queue',
                                           queue={'queue_id': 1,
                                                  'timeout': '2'}))

    def test_process_with_formdata(self):
        data = {'template': 'user',
                'user-user_id': 1,
                'user-timeout': '2'}

        with app.test_request_context(method='POST', data=data):
            form = TemplateDestinationForm()

        assert_that(form.data, has_entries(template='user',
                                           user={'user_id': 1,
                                                 'timeout': '2'}))

    def test_process_with_formdata_and_undefined_form(self):
        data = {'template': 'queue',
                'queue-queue_id': 1,
                'queue-timeout': '2'}

        with app.test_request_context(method='POST', data=data):
            form = TemplateDestinationForm()

        assert_that(form.data, has_entries(template='queue',
                                           queue={'queue_id': '1',
                                                  'timeout': '2'}))

    def test_process_without_select_field(self):
        data = {'template': 'none'}

        with app.test_request_context():
            form = BaseDestinationForm(**data)

        assert_that(form.data, empty())


class TestFallbacksForm(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def test_to_dict_with_none_as_destination(self):
        data = {'busy_destination-type': 'none'}

        with app.test_request_context(method='POST', data=data):
            form = FallbacksForm()
        result = form.to_dict()

        assert_that(result, has_entries(busy_destination=None))
