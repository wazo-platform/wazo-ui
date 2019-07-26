# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    FieldList,
    FormField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm


class RulesDefinitionForm(BaseForm):
    definition = TextAreaField(l_('Rule'), [InputRequired()])


class SkillRuleForm(BaseForm):
    name = StringField(l_('Name'), [InputRequired(), Length(max=64)])
    rules = FieldList(FormField(RulesDefinitionForm))
    submit = SubmitField(l_('Submit'))
