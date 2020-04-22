# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    SubmitField,
    StringField,
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    SelectField,
    SelectMultipleField
)
from wtforms.validators import InputRequired, Email

from wazo_ui.helpers.form import BaseForm


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
        choices=[
            ('user', l_('User')),
            ('external_api', l_('External API'))
        ]
    )
    submit = SubmitField()


class GroupForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    members = FormField(MembersForm)
    tenant_uuid = SelectField(l_('Tenant'), choices=[])
    tenant = FormField(TenantUuidForm)
    submit = SubmitField()


class TenantForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    members = FormField(MembersForm)
    submit = SubmitField()


class AclTemplatesForm(BaseForm):
    acl = StringField(validators=[InputRequired()])


class PolicyForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    description = StringField(l_('Description'))
    acl_templates = FieldList(FormField(AclTemplatesForm))
    tenant_uuid = SelectField(l_('Tenant'), choices=[])
    tenant = FormField(TenantUuidForm)
    submit = SubmitField()
