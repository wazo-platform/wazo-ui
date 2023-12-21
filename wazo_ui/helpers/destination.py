# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from werkzeug.datastructures import ImmutableMultiDict
from wtforms.fields import FormField, HiddenField, SelectField, StringField
from wtforms.utils import unset_value

from wazo_ui.helpers.form import BaseForm

from .view import listing_urls

_destination_choices = []


def register_destination_form(type_id, type_label, form, position=-1):
    if (type_id, type_label) not in _destination_choices:
        _destination_choices.insert(position, (type_id, type_label))

    if getattr(form, 'select_field', False):
        setattr(DestinationForm, type_id, DestinationField(destination_form=form))
    else:
        setattr(DestinationForm, type_id, FormField(form))


class BaseDestinationForm(BaseForm):
    select_field = None

    def __init__(self, *args, **kwargs):
        self.added_dynamic_choice = ()
        super().__init__(*args, **kwargs)

    def to_dict(self):
        if not self.select_field or not getattr(self, self.select_field, False):
            return {}

        data = super().to_dict()

        selected_value = data.get(self.select_field)
        if not selected_value:
            return {}

        selected_args = data.get(selected_value, {})
        result = self._convert_all_empty_string_to_none(selected_args)
        result[self.select_field] = selected_value
        return result

    def _convert_all_empty_string_to_none(self, data):
        result = {}
        for key, val in data.items():
            result[key] = val if val != '' else None
        return result

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        if not self.select_field or not getattr(self, self.select_field, False):
            return

        selected_value = kwargs.pop(self.select_field, None)
        selected_args = kwargs
        wrapped_formdata = self.meta.wrap_formdata(self, formdata)
        if wrapped_formdata and isinstance(wrapped_formdata, ImmutableMultiDict):
            selected_value = wrapped_formdata.get(self._prefix + self.select_field, '')
            key_prefix = self._prefix + selected_value + '-'
            selected_args = {
                k[len(key_prefix) :]: v
                for k, v in wrapped_formdata.items()
                if key_prefix in k
            }

        if selected_value:
            kwargs = {self.select_field: selected_value, selected_value: selected_args}
            if not getattr(self, selected_value, False):
                self._create_dynamic_destination_form(kwargs)

        super().process(formdata, obj, data, **kwargs)

    def _create_dynamic_destination_form(self, destination):
        class DynamicForm(BaseForm):
            pass

        for key in destination[destination[self.select_field]]:
            setattr(DynamicForm, key, StringField())

        options = dict(
            name=destination[self.select_field],
            prefix=self._prefix,
            translations=self.meta.get_translations(self),
        )
        field = self.meta.bind_field(self, FormField(DynamicForm), options)
        self._fields[destination[self.select_field]] = field
        self.added_dynamic_choice = (
            destination[self.select_field],
            destination[self.select_field],
        )


class DestinationForm(BaseDestinationForm):
    select_field = 'type'

    type = SelectField(l_('Destination'), choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = _destination_choices
        self.listing_urls = listing_urls


class DestinationField(FormField):
    def __init__(self, *args, **kwargs):
        self.destination_label = kwargs.pop('destination_label', None)
        self.destination_form = kwargs.pop('destination_form', DestinationForm)
        super().__init__(self.destination_form, *args, **kwargs)

    def process(self, formdata, data=unset_value):
        super().process(formdata, data)
        if self.destination_label is not None:
            self.form.type.label.text = self.destination_label


class FallbacksForm(BaseForm):
    busy_destination = DestinationField(l_('Busy'))
    congestion_destination = DestinationField(l_('Congestion'))
    fail_destination = DestinationField(l_('Fail'))
    noanswer_destination = DestinationField(l_('No answer'))

    def to_dict(self):
        data = super().to_dict()

        for key, val in data.items():
            if val.get('type') == 'none':
                data[key] = None
        return data


class DestinationHiddenField(HiddenField):
    def __init__(self, *args, **kwargs):
        def remove_none(value):
            return value or ''

        super().__init__(filters=[remove_none], *args, **kwargs)
