# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm


class SkillForm(BaseForm):
    category = StringField(l_('Category'), [InputRequired(), Length(max=64)])
    name = StringField(l_('Name'), [InputRequired(), Length(max=64)])
    description = StringField(l_('Description'), [Length(max=128)])
    submit = SubmitField(l_('Submit'))
