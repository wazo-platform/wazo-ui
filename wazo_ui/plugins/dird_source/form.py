# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FormField,
    BooleanField,
    FieldList,
    FloatField,
    SubmitField,
    StringField,
    SelectField,
    HiddenField,
)
from wtforms.validators import InputRequired
from wtforms.widgets import PasswordInput

from wazo_ui.helpers.form import BaseForm

column_formats = [('string', 'String'), ('binary_uuid', 'Binary Uuid')]


class ValueColumnsForm(BaseForm):
    key = StringField(validators=[InputRequired()])
    value = StringField(validators=[InputRequired()])


class ColumnsForm(BaseForm):
    value = StringField(validators=[InputRequired()])


class CsvForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))
    # `separator` can't be used an a field for wtforms ...
    delimiter = StringField(l_('Delimiter'))
    file = StringField(l_('File'), validators=[InputRequired()])
    unique_column = StringField(l_('Unique column'))


class CsvWsForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))
    # `separator` can't be used an a field for wtforms ...
    delimiter = StringField(l_('Delimiter'))
    list_url = StringField(l_('List URL'))
    lookup_url = StringField(l_('Lookup URL'), validators=[InputRequired()])
    timeout = FloatField(l_('Timeout'))
    unique_column = StringField(l_('Unique column'))


class LdapForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    ldap_base_dn = StringField(
        l_('Base DN'),
        validators=[InputRequired()],
        default='ou=people,dc=example,dc=com',
    )
    custom_filter = StringField(l_('Custom filter'))
    ldap_password = StringField(l_('Password'), widget=PasswordInput(hide_value=False))
    ldap_uri = StringField(l_('Uri'), validators=[InputRequired()])
    ldap_username = StringField(
        l_('Username'),
        validators=[InputRequired()],
        default='cn=admin,dc=example,dc=org',
    )
    searched_columns = FieldList(FormField(ColumnsForm))
    unique_column = StringField(l_('Unique column'))
    unique_column_format = SelectField('Unique column format', choices=column_formats)


class Office365AuthForm(BaseForm):
    host = StringField(l_('Host'))
    port = StringField(l_('Port'))
    prefix_ = StringField(l_('Prefix'))
    https = BooleanField(l_('SSL/TLS'), default=False)
    verify_certificate = BooleanField(l_('Verify certificate'), default=False)
    certificate_path = StringField(l_('Certificate path'))
    version = StringField(l_('Version'))


class Office365Form(BaseForm):
    auth = FormField(Office365AuthForm)
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))
    endpoint = StringField(l_('Endpoint'))


class GoogleAuthForm(BaseForm):
    host = StringField(l_('Host'))
    port = StringField(l_('Port'))
    prefix_ = StringField(l_('Prefix'))
    https = BooleanField(l_('SSL/TLS'), default=False)
    verify_certificate = BooleanField(l_('Verify certificate'), default=False)
    certificate_path = StringField(l_('Certificate path'))
    version = StringField(l_('Version'))


class GoogleForm(BaseForm):
    auth = FormField(GoogleAuthForm)
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))


class PersonalForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))


class PhonebookForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))
    phonebook_uuid = SelectField(l_('Phonebook'), choices=[])
    phonebook_name = HiddenField()


class WazoAuthForm(BaseForm):
    host = StringField(l_('Host'))
    port = StringField(l_('Port'))
    prefix_ = StringField(l_('Prefix'))
    https = BooleanField(l_('SSL/TLS'), default=False)
    verify_certificate = BooleanField(l_('Verify certificate'), default=False)
    certificate_path = StringField(l_('Certificate path'))
    timeout = FloatField(l_('Timeout'))
    key_file = StringField(l_('Key file'))
    username = StringField(l_('Username'))
    password = StringField(l_('Password'), widget=PasswordInput(hide_value=False))
    version = StringField(l_('Version'))


class WazoConfdForm(BaseForm):
    host = StringField(l_('Host'))
    port = StringField(l_('Port'))
    prefix_ = StringField(l_('Prefix'))
    verify_certificate = BooleanField(l_('Verify certificate'), default=False)
    certificate_path = StringField(l_('Certificate path'))
    timeout = FloatField(l_('Timeout'))
    https = BooleanField(l_('Https'), default=False)
    version = StringField(l_('Version'))


class WazoForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))
    auth = FormField(WazoAuthForm)
    confd = FormField(WazoConfdForm)


class ConferenceForm(BaseForm):
    first_matched_columns = FieldList(FormField(ColumnsForm))
    format_columns = FieldList(FormField(ValueColumnsForm))
    searched_columns = FieldList(FormField(ColumnsForm))
    auth = FormField(WazoAuthForm)
    confd = FormField(WazoConfdForm)


class DirdSourceForm(BaseForm):
    tenant_uuid = HiddenField()
    backend = HiddenField()
    name = StringField(l_('Name'), validators=[InputRequired()])
    ldap_config = FormField(LdapForm)
    conference_config = FormField(ConferenceForm)
    csv_config = FormField(CsvForm)
    csv_ws_config = FormField(CsvWsForm)
    office365_config = FormField(Office365Form)
    google_config = FormField(GoogleForm)
    personal_config = FormField(PersonalForm)
    phonebook_config = FormField(PhonebookForm)
    wazo_config = FormField(WazoForm)
    submit = SubmitField()
