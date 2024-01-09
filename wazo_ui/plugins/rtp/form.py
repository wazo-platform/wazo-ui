# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired

from wazo_ui.helpers.form import BaseForm


class OptionsForm(BaseForm):
    option_key = StringField(validators=[InputRequired()])
    option_value = StringField(validators=[InputRequired()])


class RtpForm(BaseForm):
    rtpstart = StringField(l_('RTP Start'))
    rtpend = StringField(l_('RTP End'))
    rtpchecksums = SelectField(
        l_('RTP Check Sums'), choices=[('no', l_('No')), ('yes', l_('Yes'))]
    )
    dtmftimeout = StringField(l_('DTMF Timeout'))
    rtcpinterval = StringField(l_('RTCP Interval'))
    strictrtp = SelectField(
        l_('Strict RTP'),
        choices=[('no', l_('No')), ('yes', l_('Yes')), ('seqno', l_('Seqno'))],
    )
    probation = StringField(l_('Probation'))
    icesupport = SelectField(
        l_('Ice Support'), choices=[('no', l_('No')), ('yes', l_('Yes'))]
    )
    stunaddr = StringField(l_('STUN Address'))
    stun_blacklist = StringField(l_('STUN Blacklist'))
    turnaddr = StringField(l_('TURN Address'))
    turnusername = StringField(l_('TURN Username'))
    turnpassword = StringField(l_('TURN Password'))
    ice_blacklist = StringField(l_('Ice Blacklist'))
    ice_host_candidates = FieldList(FormField(OptionsForm))
    submit = SubmitField(l_('Submit'))
