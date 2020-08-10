# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    HiddenField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length

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


class LineForm(BaseForm):
    context = SelectField(l_('Context'), validators=[InputRequired()], choices=[])
    protocol = SelectField(choices=[('sip', l_('SIP')), ('custom', l_('CUSTOM'))])
    endpoint_sip = FormField(EnpointSipForm)
    endpoint_custom = FormField(EnpointCustomForm)
    submit = SubmitField(l_('Submit'))
