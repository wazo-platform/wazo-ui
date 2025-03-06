# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from wtforms.fields import StringField, SubmitField

from wazo_ui.helpers.form import BaseForm


class RecordingAnnouncementForm(BaseForm):
    recording_start = StringField(l_('Start Announcement'))
    recording_stop = StringField(l_('Stop Announcement'))
    submit = SubmitField(l_('Submit'))
