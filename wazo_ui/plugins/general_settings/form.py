# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    SelectField,
    StringField,
    SubmitField
)
from wtforms.validators import InputRequired, IPAddress

from wazo_ui.helpers.form import BaseForm


class BasePJSIPOptionsForm(BaseForm):
    def to_dict(self):
        return super().to_dict(empty_string=True)

    option_key = SelectField(
        choices=[],
        validators=[InputRequired()],
    )
    option_value = StringField()


class PJSIPGlobalOptionsForm(BasePJSIPOptionsForm):
    pass


class PJSIPSystemOptionsForm(BasePJSIPOptionsForm):
    pass


class OptionsForm(BaseForm):

    def to_dict(self):
        return super().to_dict(empty_string=True)

    option_key = StringField(validators=[InputRequired()])
    option_value = StringField()


class OrderedOptionsForm(BaseForm):

    def to_dict(self):
        return super().to_dict(empty_string=True)

    option_key = StringField(validators=[InputRequired()])
    option_value = StringField()


class GeneralSettingsOptionsForm(BaseForm):
    options = FieldList(FormField(OptionsForm))
    ordered_options = FieldList(FormField(OptionsForm))


class SipGeneralSettingsForm(GeneralSettingsOptionsForm):
    submit = SubmitField(l_('Submit'))


class PJSIPGlobalSettingsForm(BaseForm):
    options = FieldList(FormField(PJSIPGlobalOptionsForm))
    submit = SubmitField(l_('Submit'))


class PJSIPSystemSettingsForm(BaseForm):
    options = FieldList(FormField(PJSIPSystemOptionsForm))
    submit = SubmitField(l_('Submit'))


class IaxCallnumberlimitsForm(BaseForm):
    ip_address = StringField(l_('IP Address'), validators=[IPAddress()])
    netmask = StringField(l_('Netmask'))
    limit = StringField(l_('Limit'))


class IaxGeneralSettingsForm(BaseForm):
    general = FormField(GeneralSettingsOptionsForm)
    callnumberlimits = FieldList(FormField(IaxCallnumberlimitsForm))
    submit = SubmitField(l_('Submit'))


class SccpGeneralSettingsForm(GeneralSettingsOptionsForm):
    submit = SubmitField(l_('Submit'))


class VoicemailZonemessages(BaseForm):
    name = StringField(l_('Name'))
    timezone = SelectField(
        l_('Timezone'),
        validators=[InputRequired()],
        choices=[
            ('America/St_Johns', 'America/St_Johns'),
            ('America/Halifax', 'America/Halifax'),
            ('America/New_York', 'America/New_York'),
            ('America/Chicago', 'America/Chicago'),
            ('America/Denver', 'America/Denver'),
            ('America/Los_Angeles', 'America/Los_Angeles'),
            ('America/Anchorage', 'America/Anchorage'),
            ('Europe/Paris', 'Europe/Paris'),
        ]
    )
    message = StringField(l_('Message'))


class VoicemailGeneralSettingsForm(BaseForm):
    general = FormField(GeneralSettingsOptionsForm)
    zonemessages = FieldList(FormField(VoicemailZonemessages))
    submit = SubmitField(l_('Submit'))


class FeaturesGeneralSettingsForm(BaseForm):
    general = FormField(GeneralSettingsOptionsForm)
    featuremap = FormField(GeneralSettingsOptionsForm)
    applicationmap = FormField(GeneralSettingsOptionsForm)
    submit = SubmitField(l_('Submit'))


class ConfBridgeGeneralSettingsForm(BaseForm):
    wazo_default_bridge = FormField(GeneralSettingsOptionsForm)
    wazo_default_user = FormField(GeneralSettingsOptionsForm)
    submit = SubmitField(l_('Submit'))
