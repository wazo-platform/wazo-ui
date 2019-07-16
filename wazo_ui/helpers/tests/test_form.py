# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from flask import Flask
from wtforms.fields import FieldList, FormField, StringField, SubmitField

from hamcrest import (
    assert_that,
    contains,
    equal_to,
    empty,
    has_entries,
    has_key,
    has_properties,
    has_property,
    instance_of,
    not_,
)

from ..form import BaseForm, SelectField


app = Flask('test_wazo_ui')


class TestBaseForm(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def test_to_dict_with_csrf_token(self):
        class MyForm(BaseForm):
            attribute1 = StringField()
            csrf_token = StringField()

        with app.test_request_context(method='POST', data={'attribute1': 'value',
                                                           'csrf_token': '123-abcd'}):
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute1='value'))

    def test_to_dict_with_submitfield(self):
        class MyForm(BaseForm):
            attribute1 = StringField()
            submit = SubmitField()

        with app.test_request_context(method='POST', data={'attribute1': 'value',
                                                           'submit': 'true'}):
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute1='value'))

    def test_to_dict_with_default_and_empty_data(self):
        class MyForm(BaseForm):
            attribute1 = StringField(default='default')

        with app.test_request_context(method='POST', data={'attribute1': ''}):
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute1='default'))

    def test_to_dict_with_default_and_data(self):
        class MyForm(BaseForm):
            attribute1 = StringField(default='default')

        with app.test_request_context(method='POST', data={'attribute1': 'value'}):
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute1='value'))

    def test_to_dict_with_default_and_no_data(self):
        class MyForm(BaseForm):
            attribute1 = StringField(default='default')

        with app.test_request_context():
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute1='default'))

    def test_to_dict_with_default_to_false_and_no_data(self):
        class MyForm(BaseForm):
            attribute1 = StringField(default=False)

        with app.test_request_context():
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute1=False))

    def test_to_dict_with_no_data(self):
        class MyForm(BaseForm):
            attribute1 = StringField()

        with app.test_request_context():
            form = MyForm()
        result = form.to_dict()

        assert_that(result, not_(has_key('attribute1')))

    def test_to_dict_with_empty_data(self):
        class MyForm(BaseForm):
            attribute1 = StringField()

        with app.test_request_context(method='POST', data={'attribute1': ''}):
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute1=None))

    def test_to_dict_with_formfield(self):
        class SubMyForm(BaseForm):
            subattribute = StringField()

        class MyForm(BaseForm):
            attribute = FormField(SubMyForm)

        with app.test_request_context(method='POST', data={'attribute-subattribute': 'subvalue'}):
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute=has_entries(subattribute='subvalue')))

    def test_to_dict_with_listfield_of_fieldform(self):
        class SubMyForm(BaseForm):
            subattribute = StringField()

        class MyForm(BaseForm):
            attribute = FieldList(FormField(SubMyForm))

        with app.test_request_context(method='POST', data={'attribute-0-subattribute': 'subvalue'}):
            form = MyForm()
        result = form.to_dict()

        assert_that(result, has_entries(attribute=contains(has_entries(subattribute='subvalue'))))

    def test_to_dict_with_default_empty_data(self):
        class MyForm(BaseForm):
            attribute1 = StringField(default='')

        with app.test_request_context():
            form = MyForm()
        result = form.to_dict(empty_string=True)

        assert_that(result, has_entries(attribute1=''))

    def test_populate_errors(self):
        class MyForm(BaseForm):
            attribute1 = StringField()
            attribute2 = StringField()

        errors = {'attribute1': 'error1',
                  'attribute2': 'error2'}

        with app.test_request_context():
            form = MyForm()
        form.populate_errors(errors)

        assert_that(form, has_properties(
            attribute1=has_properties(errors=contains('error1')),
            attribute2=has_properties(errors=contains('error2')),
        ))

    def test_populate_errors_when_error_not_match_field(self):
        class MyForm(BaseForm):
            attribute1 = StringField()

        errors = {'attribute2': 'error3'}

        with app.test_request_context():
            form = MyForm()
        form.populate_errors(errors)

        assert_that(form, has_properties(attribute1=has_properties(errors=empty())))
        assert_that(form, not_(has_property('attribute2')))

    def test_populate_errors_when_formfield(self):
        class SubMyForm(BaseForm):
            subattribute1 = StringField()

        class MyForm(BaseForm):
            attribute1 = FormField(SubMyForm)

        errors = {'attribute1': {'subattribute1': 'suberror1'}}

        with app.test_request_context():
            form = MyForm()
        form.populate_errors(errors)

        assert_that(form, has_properties(
            attribute1=has_properties(form=has_properties(
                subattribute1=has_properties(errors=contains('suberror1'))
            ))
        ))

    def test_populate_errors_when_fieldlist_of_formfield(self):
        class SubMyForm(BaseForm):
            subattribute1 = StringField()

        class MyForm(BaseForm):
            attribute1 = FieldList(FormField(SubMyForm), min_entries=2)

        errors = {'attribute1': {'1': {'subattribute1': 'suberror1'}}}

        with app.test_request_context():
            form = MyForm()
        form.populate_errors(errors)

        assert_that(form, has_properties(
            attribute1=contains(
                has_properties(form=has_properties(
                    subattribute1=has_properties(errors=empty())
                )),
                has_properties(form=has_properties(
                    subattribute1=has_properties(errors=contains('suberror1'))
                )))
        ))

    def test_populate_errors_when_errors_is_initialize_with_tuple(self):
        class MyForm(BaseForm):
            attribute1 = StringField()
            attribute2 = StringField()

        with app.test_request_context():
            form = MyForm()
        form.attribute1.errors = tuple()

        errors = {'attribute1': 'error1'}
        form.populate_errors(errors)

        assert_that(form, has_properties(
            attribute1=has_properties(errors=instance_of(list))
        ))


class TestSelectField(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        class MyForm(BaseForm):
            field = SelectField()

        with app.test_request_context():
            self.field = MyForm().field

    def test_coerce_from_none(self):
        self.field.process_data(None)
        assert_that(self.field.data, equal_to(None))

    def test_coerce_from_integer(self):
        self.field.process_data(1)
        assert_that(self.field.data, equal_to('1'))

    def test_coerce_from_string(self):
        self.field.process_data('string')
        assert_that(self.field.data, equal_to('string'))
