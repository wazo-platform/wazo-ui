# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    SubmitField,
    FieldList,
    FormField,
    HiddenField,
    PasswordField,
    SelectMultipleField,
    StringField,
)
from wtforms.fields.html5 import IntegerField
from wtforms.validators import Email, InputRequired, Length

from wazo_ui.helpers.form import BaseForm, SelectField


class UserUuidForm(BaseForm):
    uuid = HiddenField()
    username = HiddenField()


class GroupUuidForm(BaseForm):
    uuid = HiddenField()
    name = HiddenField()


class TenantUuidForm(BaseForm):
    uuid = HiddenField()
    name = StringField(l_('Name'))


class PolicyUuidForm(BaseForm):
    uuid = HiddenField()
    name = HiddenField()


class MembersForm(BaseForm):
    user_uuids = SelectMultipleField(l_('Members'), choices=[])
    users = FieldList(FormField(UserUuidForm))
    group_uuids = SelectMultipleField(l_('Groups'), choices=[])
    groups = FieldList(FormField(GroupUuidForm))
    policy_uuids = SelectMultipleField(l_('Policies'), choices=[])
    policies = FieldList(FormField(PolicyUuidForm))


class EmailForm(BaseForm):
    main = BooleanField(l_('Main'), default=False)
    address = StringField(l_('Address'), validators=[Email()])


class IdentityForm(BaseForm):
    username = StringField(l_('Username'), validators=[InputRequired()])
    password = StringField(l_('Password'))
    firstname = StringField(l_('Firstname'))
    lastname = StringField(l_('Lastname'))
    email_address = StringField(l_('Email'))
    emails = FieldList(FormField(EmailForm))
    members = FormField(MembersForm)
    tenant_uuid = SelectField(l_('Tenant'), choices=[])
    tenant = FormField(TenantUuidForm)
    purpose = SelectField(
        l_('Purpose'),
        choices=[('user', l_('User')), ('external_api', l_('External API'))],
    )
    submit = SubmitField()


class GroupForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    members = FormField(MembersForm)
    tenant_uuid = SelectField(l_('Tenant'), choices=[])
    tenant = FormField(TenantUuidForm)
    submit = SubmitField()


class DomainNameForm(BaseForm):
    name = StringField('', validators=[Length(max=253)])


class TenantForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    slug = StringField(l_('Identifier'))
    domains = FieldList(FormField(DomainNameForm))
    domain_names = FieldList(StringField(l_('Domain Names')))  # Read-Only
    members = FormField(MembersForm)
    submit = SubmitField()


class AccessForm(BaseForm):
    value = StringField(validators=[InputRequired()])


class PolicyForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    description = StringField(l_('Description'))
    acl = FieldList(FormField(AccessForm))
    tenant_uuid = SelectField(l_('Tenant'), choices=[])
    tenant = FormField(TenantUuidForm)
    submit = SubmitField()


class LDAPForm(BaseForm):
    host = StringField(l_('Host'), validators=[InputRequired(), Length(max=512)])
    port = IntegerField(l_('Port'), validators=[InputRequired()])
    protocol_version = SelectField(
        l_('Protocol version'),
        coerce=int,
        choices=[(2, '2'), (3, '3')],
        default=3,
    )
    protocol_security = SelectField(
        l_('Protocol security'),
        choices=[('tls', l_('TLS')), ('ldaps', l_('LDAPS')), (None, l_('None'))],
    )
    bind_dn = StringField(l_('Bind DN'), validators=[Length(max=256)])
    bind_password = PasswordField(l_('Bind password'))
    user_base_dn = StringField(
        l_('User base DN'), validators=[InputRequired(), Length(max=256)]
    )
    user_login_attribute = StringField(
        l_('User login attribute'), validators=[InputRequired(), Length(max=64)]
    )
    user_email_attribute = StringField(
        l_('User email attribute'), validators=[InputRequired(), Length(max=64)]
    )
    search_filters = StringField(l_('Search filters'))

    submit = SubmitField()
