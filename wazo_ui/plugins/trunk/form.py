# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    IntegerField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import PasswordInput

from wazo_ui.helpers.form import BaseForm
from wazo_ui.plugins.sip_template.form import (
    BasePJSIPOptionsForm,
    IdentifyPJSIPOptionsForm,
    RegistrationPJSIPOptionsForm,
    TransportForm,
    TemplateForm,
)


class EnpointCustomForm(BaseForm):
    id = HiddenField()
    interface = StringField(l_('Interface'), validators=[InputRequired()])
    interface_suffix = StringField(l_('Interface Suffix'), validators=[Length(max=32)])


class OptionsForm(BaseForm):
    option_key = StringField(validators=[InputRequired()])
    option_value = StringField(validators=[InputRequired()])


class EnpointSipForm(BaseForm):
    uuid = HiddenField()
    label = StringField(l_('Label'), validators=[InputRequired(), Length(max=128)])
    name = StringField(l_('Name'), [Length(max=128)])
    aor_section_options = FieldList(FormField(BasePJSIPOptionsForm))
    auth_section_options = FieldList(FormField(BasePJSIPOptionsForm))
    endpoint_section_options = FieldList(FormField(BasePJSIPOptionsForm))
    identify_section_options = FieldList(FormField(IdentifyPJSIPOptionsForm))
    registration_section_options = FieldList(FormField(RegistrationPJSIPOptionsForm))
    registration_outbound_auth_section_options = FieldList(FormField(BasePJSIPOptionsForm))
    outbound_auth_section_options = FieldList(FormField(BasePJSIPOptionsForm))
    transport = FormField(TransportForm)
    template_uuids = SelectMultipleField(l_('Templates'), choices=[])
    templates = FieldList(FormField(TemplateForm))


class EnpointIaxForm(BaseForm):
    id = HiddenField()
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=40)])
    type = SelectField(l_('Type'), choices=[('user', l_('User')), ('peer', l_('Peer')), ('friend', l_('Friend'))])
    host = SelectField(l_('Host'), validators=[InputRequired(), Length(max=255)],
                       choices=[('dynamic', l_('Dynamic')), ('static', l_('Static'))])
    host_value = StringField('', validators=[Length(max=255)])
    options = FieldList(FormField(OptionsForm))


class RegisterIAXForm(BaseForm):
    id = HiddenField()
    enabled = BooleanField(l_('Enabled'), default=False)
    auth_username = StringField(l_('Authentication Username'))
    auth_password = StringField(l_('Authentication Password'), widget=PasswordInput(hide_value=False))
    callback_context = StringField(l_('Callback Context'))
    callback_extension = StringField(l_('Callback Extension'))
    remote_host = StringField(l_('Remote Host'), validators=[InputRequired()])
    remote_port = IntegerField(l_('Remote port'))


class TrunkForm(BaseForm):
    context = SelectField(l_('Context'), choices=[])
    protocol = SelectField(choices=[('sip', l_('SIP')), ('iax', l_('IAX')), ('custom', l_('CUSTOM'))])
    endpoint_sip = FormField(EnpointSipForm)
    endpoint_iax = FormField(EnpointIaxForm)
    endpoint_custom = FormField(EnpointCustomForm)
    register_iax = FormField(RegisterIAXForm)
    submit = SubmitField(l_('Submit'))
