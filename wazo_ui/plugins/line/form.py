# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FormField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
    FieldList,
)
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm
from wazo_ui.plugins.sip_template.form import EndpointSIPForm


class SCCPOptionsForm(BaseForm):
    option_key = SelectField(choices=[], validators=[InputRequired()])
    option_value = StringField(validators=[InputRequired()])


class EndpointSCCPForm(BaseForm):
    id = HiddenField()
    options = FieldList(FormField(SCCPOptionsForm))


class EndpointCustomForm(BaseForm):
    id = HiddenField()
    interface = StringField(l_('Interface'), validators=[InputRequired()])
    interface_suffix = StringField(l_('Interface Suffix'), validators=[Length(max=32)])


class LineForm(BaseForm):
    context = SelectField(l_('Context'), validators=[InputRequired()], choices=[])
    protocol = SelectField(
        choices=[('sip', l_('SIP')), ('sccp', l_('SCCP')), ('custom', l_('CUSTOM'))]
    )
    endpoint_sip = FormField(EndpointSIPForm)
    endpoint_sccp = FormField(EndpointSCCPForm)
    endpoint_custom = FormField(EndpointCustomForm)
    submit = SubmitField(l_('Submit'))
