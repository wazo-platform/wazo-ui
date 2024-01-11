# Copyright 2021-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import HiddenField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm


class PhonebookForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=80)])
    description = StringField(l_('Description'), [Length(max=80)])
    submit = SubmitField(l_('Submit'))


class ManagePhonebookForm(BaseForm):
    firstname = StringField(l_('Firstname'), [InputRequired(), Length(max=80)])
    lastname = StringField(l_('Lastname'), [InputRequired(), Length(max=80)])
    email = StringField(l_('Email'), [Length(max=80)])
    phone = StringField(l_('Phone'), [InputRequired(), Length(max=80)])
    mobile_phone = StringField(l_('Mobile Phone'), [Length(max=80)])
    fax = StringField(l_('Fax'), [Length(max=80)])
    phonebook_uuid = HiddenField()
    submit = SubmitField(l_('Submit'))
