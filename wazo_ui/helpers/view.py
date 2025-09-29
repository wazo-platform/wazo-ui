# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from flask import flash, request

from wazo_ui.helpers.classful import (
    DEFAULT_TEMPLATE,
    BaseView,
    IndexAjaxViewMixin,
    NewViewMixin,
)

from .error import ConfdErrorExtractor as e_extractor
from .error import ConfdErrorTranslator as e_translator

logger = logging.getLogger(__name__)
listing_urls = {}


def register_listing_url(type_id, endpoint):
    listing_urls[type_id] = endpoint


class BaseEngineView:
    listing_urls = listing_urls

    def _get_template(self, type_):
        blueprint = request.blueprint.replace('.', '/')
        return self.templates.get(
            type_, DEFAULT_TEMPLATE.format(blueprint=blueprint, type_=type_)
        )


class IndexAjaxHelperViewMixin(BaseEngineView, IndexAjaxViewMixin):
    pass


class BaseIPBXHelperView(BaseEngineView, BaseView):
    def _fill_form_error(self, form, error):
        response = error.response.json()
        error_id = e_extractor.extract_generic_error_id(response)
        if error_id == 'invalid-data':
            error_fields = e_extractor.extract_fields(response)
            error_field_ids = e_extractor.extract_specific_error_id_from_fields(
                error_fields
            )
            error_field_messages = e_translator.translate_specific_error_id_from_fields(
                error_field_ids
            )

            resource = e_extractor.extract_resource(error.request)
            form = self._map_resources_to_form_errors(
                form, {resource: error_field_messages}
            )
        return form

    def _flash_http_error(self, error):
        try:
            response = error.response.json()
            resource = e_extractor.extract_resource(error.request)
            error_id = e_extractor.extract_generic_error_id(response)

            translated_resource = e_translator.resources.get(resource, '')
            flash(
                f'{translated_resource}{": " if translated_resource else ""}'
                f'{e_translator.generic_messages.get(error_id, "")}',
                'error',
            )
            flash(
                f'{error.request.method} {error.request.url}: {response}',
                'error_details',
            )
        except Exception:
            flash(error, 'error')


class NewHelperViewMixin(BaseEngineView, NewViewMixin):
    pass
