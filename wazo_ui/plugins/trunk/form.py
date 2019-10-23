# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import PasswordInput

from wazo_ui.helpers.form import BaseForm


class EnpointCustomForm(BaseForm):
    id = HiddenField()
    interface = StringField(l_('Interface'), validators=[InputRequired()])
    interface_suffix = StringField(l_('Interface Suffix'), validators=[Length(max=32)])


class OptionsForm(BaseForm):
    option_key = StringField(validators=[InputRequired()])
    option_value = StringField(validators=[InputRequired()])


class EnpointSipForm(BaseForm):
    id = HiddenField()
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=40)])
    username = StringField(l_('Username'), validators=[InputRequired(), Length(max=40)])
    secret = StringField(l_('Password'), validators=[Length(max=80)], widget=PasswordInput(hide_value=False))
    type = SelectField(l_('Type'), choices=[('user', l_('User')), ('peer', l_('Peer')), ('friend', l_('Friend'))])
    host = SelectField(l_('Host'), validators=[InputRequired(), Length(max=255)],
                       choices=[('dynamic', l_('Dynamic')), ('static', l_('Static'))])
    host_value = StringField('', validators=[Length(max=255)])
    options = FieldList(FormField(OptionsForm))


class EnpointIaxForm(BaseForm):
    id = HiddenField()
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=40)])
    type = SelectField(l_('Type'), choices=[('user', l_('User')), ('peer', l_('Peer')), ('friend', l_('Friend'))])
    host = SelectField(l_('Host'), validators=[InputRequired(), Length(max=255)],
                       choices=[('dynamic', l_('Dynamic')), ('static', l_('Static'))])
    host_value = StringField('', validators=[Length(max=255)])
    options = FieldList(FormField(OptionsForm))


class RegisterSIPForm(BaseForm):
    id = HiddenField()
    enabled = BooleanField(l_('Enabled'), default=False)
    sip_username = StringField(l_('SIP Username'), validators=[InputRequired()])
    auth_username = StringField(l_('Authentication Username'))
    auth_password = StringField(l_('Authentication Password'), widget=PasswordInput(hide_value=False))
    remote_host = StringField(l_('Remote Host'), validators=[InputRequired()])
    remote_port = IntegerField(l_('Remote port'))
    transport = SelectField(l_('Transport'), choices=[
        ('', l_('None')),
        ('tcp', l_('TCP')),
        ('tls', l_('TLS')),
        ('udp', l_('UDP')),
        ('ws', l_('WS')),
        ('wss', l_('WSS'))
    ])
    callback_extension = StringField(l_('Callback Extension'))
    expiration = IntegerField(l_('Expiration'))


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
    register_sip = FormField(RegisterSIPForm)
    register_iax = FormField(RegisterIAXForm)
    submit = SubmitField(l_('Submit'))
