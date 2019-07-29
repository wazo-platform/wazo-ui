# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.utils import unset_value
from wtforms.fields import FormField, SelectField

from wazo_ui.helpers.destination import BaseDestinationForm, listing_urls


_funckey_destination_choices = []


def register_funckey_destination_form(type_id, type_label, form, position=-1):
    if (type_id, type_label) not in _funckey_destination_choices:
        _funckey_destination_choices.insert(position, (type_id, type_label))

    if getattr(form, 'select_field', False):
        setattr(FuncKeyDestinationForm, type_id, FuncKeyDestinationField(destination_form=form))
    else:
        setattr(FuncKeyDestinationForm, type_id, FormField(form))


class FuncKeyDestinationForm(BaseDestinationForm):
    select_field = 'type'

    type = SelectField(l_('Destination'), choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type.choices = _funckey_destination_choices
        self.listing_urls = listing_urls


class FuncKeyDestinationField(FormField):

    def __init__(self, *args, **kwargs):
        self.destination_label = kwargs.pop('destination_label', None)
        self.destination_form = kwargs.pop('destination_form', FuncKeyDestinationForm)
        super().__init__(self.destination_form, *args, **kwargs)

    def process(self, formdata, data=unset_value):
        super().process(formdata, data)
        if self.destination_label is not None:
            self.form.type.label.text = self.destination_label
