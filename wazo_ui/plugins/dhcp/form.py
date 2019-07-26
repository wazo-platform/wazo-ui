# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    SubmitField,
    StringField,
)
from wtforms.validators import InputRequired

from wazo_ui.helpers.form import BaseForm


class DhcpForm(BaseForm):
    active = BooleanField(l_('Enabled'), default=False)
    network_interfaces = StringField(l_('Network interface'))
    pool_start = StringField(l_('Pool start'), validators=[InputRequired()])
    pool_end = StringField(l_('Pool end'), validators=[InputRequired()])
    submit = SubmitField(l_('Submit'))
