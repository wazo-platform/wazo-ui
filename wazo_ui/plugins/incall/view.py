# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.view import BaseIPBXHelperView
from wazo_ui.helpers.menu import menu_item

from .form import IncallForm


class IncallView(BaseIPBXHelperView):
    form = IncallForm
    resource = 'incall'

    @menu_item('.ipbx.call_management', l_('Call Management'), order=2, icon="phone", multi_tenant=True)
    @menu_item('.ipbx.call_management.incalls', l_('Incalls'), order=1, icon="arrow-right", multi_tenant=True)
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.extensions[0].exten.choices = self._build_set_choices_exten(form.extensions[0])
        form.extensions[0].context.choices = self._build_set_choices_context(form.extensions[0])
        form.schedules[0].form.id.choices = self._build_set_choices_schedule(form.schedules[0])
        sounds = self.service.list_sound()
        form.greeting_sound.choices = self._build_set_choices_sound(sounds)
        return form

    def _build_set_choices_exten(self, extension):
        if not extension.exten.data or extension.exten.data == 'None':
            return []
        return [(extension.exten.data, extension.exten.data)]

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            context = self.service.get_first_incall_context()
        else:
            context = self.service.get_context(extension.context.data)

        if context:
            return [(context['name'], context['label'])]

        return [(extension.context.data, extension.context.data)]

    def _build_set_choices_schedule(self, schedule):
        if not schedule.form.id.data or schedule.form.id.data == 'None':
            return []
        return [(schedule.form.id.data, schedule.form.name.data)]

    def _build_set_choices_sound(self, sounds):
        results = [('', l_('None'))]
        for sound in sounds['items']:
            for file_ in sound['files']:
                for format_ in file_['formats']:
                    name = format_['path'] if sound['name'] != 'system' else file_['name']
                    label = self._prepare_sound_filename_label(file_, format_)
                    results.append((name, label))
        return results

    def _prepare_sound_filename_label(self, file_, format_):
        return '{}{}{}'.format(
            file_['name'],
            ' [{}]'.format(format_['format']) if format_['format'] else '',
            ' ({})'.format(format_['language']) if format_['language'] else '',
        )

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('incall', {}))
        form.extensions[0].populate_errors(resources.get('extension', {}))
        return form
