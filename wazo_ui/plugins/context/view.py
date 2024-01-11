# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import jsonify, request
from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    build_select2_response,
    extract_select2_params,
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import ContextForm


class ContextView(BaseIPBXHelperView):
    resource = 'context'
    form = ContextForm

    @menu_item(
        '.ipbx.advanced.contexts', l_('Contexts'), icon="random", multi_tenant=True
    )
    def index(self):
        return super().index()

    def _map_resources_to_form(self, resource):
        contexts = [context['id'] for context in resource['contexts']]
        resource['context_ids'] = contexts
        form = self.form(data=resource)
        return form

    def _populate_form(self, form):
        form.context_ids.choices = self._build_set_choices_contexts(form.contexts)
        return form

    def _build_set_choices_contexts(self, contexts):
        return [(context.form.id.data, context.form.label.data) for context in contexts]


class ContextListingView(LoginRequiredView):
    def list_json_by_type(self, type_):
        return self._list_json(type_)

    def list_json_with_id(self):
        return self._list_json(numeric_id=True)

    def list_json(self):
        return self._list_json()

    def _list_json(self, type_=None, numeric_id=False):
        params = extract_select2_params(request.args)
        if type_:
            params['type'] = type_
        contexts = self.service.list(**params)

        results = []
        for context in contexts['items']:
            context_id = context['id'] if numeric_id else context['name']
            results.append({'id': context_id, 'text': context['label']})

        return jsonify(build_select2_response(results, contexts['total'], params))
