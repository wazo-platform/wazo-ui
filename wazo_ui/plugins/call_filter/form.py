# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    IntegerField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired

from wazo_ui.helpers.destination import DestinationField, DestinationHiddenField
from wazo_ui.helpers.form import BaseForm, SelectField

bs_strategy_map = {
    'all-surrogates-then-all-recipients': l_('All secretaries'),
    'linear-surrogates-then-all-recipients': l_('Secretaries sequentially'),
    'all-recipients-then-linear-surrogates': l_('Boss, then secretaries sequentially'),
    'all-recipients-then-all-surrogates': l_('Boss, then all secretaries'),
    'all': l_('Boss and all secretaries'),
}


class FallbacksForm(BaseForm):
    noanswer_destination = DestinationField(destination_label='')


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField(l_('Firstname'))
    lastname = HiddenField(l_('Lastname'))


class UserRecipientsForm(UserForm):
    uuid = SelectField(l_('Boss'), choices=[], validators=[InputRequired()])
    timeout = IntegerField(l_('Boss Timeout'))


class UserSurrogateForm(UserForm):
    member_id = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()


class UserSurrogatesForm(BaseForm):
    user_uuids = SelectMultipleField(
        l_('Secretaries'), choices=[], validators=[InputRequired()]
    )
    users = FieldList(FormField(UserSurrogateForm), min_entries=1)


class CallFilterForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    strategy = SelectField(
        l_('Ring Strategy'), choices=[(k, v) for k, v in bs_strategy_map.items()]
    )
    caller_id_mode = SelectField(
        l_('Caller ID mode'),
        choices=[
            ('', l_('None')),
            ('prepend', l_('Prepend')),
            ('overwrite', l_('Overwrite')),
            ('append', l_('Append')),
        ],
    )
    caller_id_name = StringField(l_('Caller ID name'))
    source = SelectField(
        l_('Call From'),
        choices=[
            ('internal', l_('Internal')),
            ('external', l_('External')),
            ('all', l_('All')),
        ],
    )
    fallbacks = FormField(FallbacksForm)
    surrogates_timeout = IntegerField(l_('Secretaries ringing time'))
    recipients_user = FormField(UserRecipientsForm)
    surrogates_user = FormField(UserSurrogatesForm)
    description = StringField(l_('Description'))
    enabled = BooleanField(l_('Enabled'))
    submit = SubmitField(l_('Submit'))


class CallFilterFuncKeyDestinationForm(BaseForm):
    set_value_template = '{filter_member_firstname} {filter_member_lastname}'

    filter_member_id = SelectField(
        l_('Call Filter Member'), [InputRequired()], choices=[]
    )
    filter_member_firstname = DestinationHiddenField()
    filter_member_lastname = DestinationHiddenField()
