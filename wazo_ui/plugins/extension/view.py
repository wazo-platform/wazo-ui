# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import (
    jsonify,
    render_template,
    request,
    flash
)
from flask_babel import gettext as _
from flask_babel import lazy_gettext as l_
from flask_classful import route
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import LoginRequiredView
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ExtensionForm, ExtensionFeaturesForm

MAX_POSSIBILITIES = 1000


class ExtensionView(BaseIPBXHelperView):
    form = ExtensionForm
    resource = 'extension'

    @menu_item('.ipbx.advanced', l_('Advanced'), order=999, icon="cogs", multi_tenant=True)
    @menu_item('.ipbx.advanced.extensions', l_('Extensions'), order=1, icon="tty", multi_tenant=True)
    def index(self):
        return super().index()

    def _populate_form(self, form):
        form.context.choices = self._build_set_choices_context(form)
        return form

    def _build_set_choices_context(self, extension):
        if not extension.context.data or extension.context.data == 'None':
            return []
        return [(extension.context.data, extension.context.data)]


class ExtensionFeaturesView(BaseIPBXHelperView):
    form = ExtensionFeaturesForm
    resource = 'extension'

    @menu_item('.ipbx.global_settings.extensions_features', l_('Extensions Features'), order=2, icon="fax")
    def index(self):
        resource = {}
        try:
            resource['extensions'] = self.service.list()['items']
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        return render_template(self._get_template('edit_features'),
                               form=self.form(data=resource))

    @route('/put', methods=['POST'])
    def put(self):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._index(form)

        resources = form.to_dict()
        try:
            self.service.update_extension_features(resources['extensions'])
        except HTTPError as error:
            self._flash_http_error(error)
            return self._index()

        flash(_('Extensions features has been updated'), 'success')
        return self._redirect_for('index')


class ExtensionListingView(LoginRequiredView):

    def list_available_exten_incall(self):
        return self._list_available_exten(context_range='incall_ranges')

    def list_available_exten_group(self):
        return self._list_available_exten(context_range='group_ranges')

    def list_available_exten_user(self):
        return self._list_available_exten(context_range='user_ranges')

    def list_available_exten_queue(self):
        return self._list_available_exten(context_range='queue_ranges')

    def list_available_exten_conference(self):
        return self._list_available_exten(context_range='conference_room_ranges')

    def _list_available_exten(self, context_range):
        search = request.args.get('term') or ''
        context = request.args.get('context')
        if not context:
            return jsonify({'results': []})

        context = self.service.get_context(context)
        if not context:
            return jsonify({'results': []})

        all_extens = set()
        for ressource_range in context[context_range]:
            try:
                start = int(ressource_range['start'])
                end = int(ressource_range['end']) + 1
            except ValueError:
                continue

            if end - start > MAX_POSSIBILITIES:
                end = start + MAX_POSSIBILITIES

            # TODO benchmark to improve this
            for v in range(start, end):
                if not search or search in str(v):
                    if context_range == 'incall_ranges':
                        all_extens.add(str(v).zfill(ressource_range['did_length']))
                    else:
                        all_extens.add(str(v))

        if not all_extens:
            return jsonify({'results': []})

        used_extens = set([])
        for extension in self.service.list(search=search, context=context['name'])['items']:
            if search and search not in extension['exten']:
                continue

            used_extens.add(extension['exten'])

        valid_extens = all_extens - used_extens
        valid_extens = sorted(valid_extens)

        results = [{'id': exten, 'text': exten} for exten in valid_extens]
        return jsonify({'results': results})
