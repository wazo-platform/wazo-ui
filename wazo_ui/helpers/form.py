# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_wtf import FlaskForm
from wtforms.fields import (
    FieldList,
    FormField,
    SelectField as WTFSelectField,
    SubmitField
)


class BaseForm(FlaskForm):

    def to_dict(self, empty_string=False):
        result = {}
        for name, f in self._fields.items():
            if name == 'csrf_token' or isinstance(f, SubmitField):
                continue
            elif isinstance(f, FormField):
                result[name] = f.form.to_dict()
            elif isinstance(f, FieldList):
                result[name] = [entry.to_dict() for entry in f.entries]
            elif not f.raw_data and f.default is None:
                continue
            else:
                default = f.default or f.data
                data = f.data if f.data else default
                result[name] = data if empty_string or data != '' else None
        return result

    def populate_errors(self, resource):
        for form_name, form_value in self._fields.items():
            if form_name not in resource:
                continue

            if isinstance(resource[form_name], list):
                for error in resource[form_name]:
                    self._populate_error_form(form_value, error)
            else:
                self._populate_error_form(form_value, resource[form_name])

    def _populate_error_form(self, form_value, error):
        if isinstance(form_value, FormField):
            form_value.form.populate_errors(error)
        elif isinstance(form_value, FieldList):
            for index, form in enumerate(form_value.entries):
                form.populate_errors(error.get(str(index), {}))
        else:
            # normally it's form.validate() that make this conversion
            form_value.errors = list(form_value.errors)

            form_value.errors.append(error)


class SelectField(WTFSelectField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('coerce', self._coerce_str_unless_none)
        super().__init__(*args, **kwargs)

    # https://github.com/wtforms/wtforms/issues/324
    def _coerce_str_unless_none(self, value):
        return str(value) if value is not None else None
