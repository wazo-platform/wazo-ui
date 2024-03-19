# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
from typing import Any, Protocol

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_babel import gettext as _
from flask_classful import FlaskView, route
from flask_login import login_required
from requests.exceptions import HTTPError

from .error import ErrorExtractor, ErrorTranslator

logger = logging.getLogger(__name__)

DEFAULT_TEMPLATE = '{blueprint}/{type_}.html'
listing_urls = {}


def register_listing_url(type_id, endpoint):
    listing_urls[type_id] = endpoint


class LoginRequiredView(FlaskView):
    decorators = [login_required]


class IndexAjaxViewMixin:
    listing_urls = listing_urls

    def _index(self, form=None):
        form = form or self.form()
        form = self._populate_form(form)

        return render_template(
            self._get_template('list'),
            form=form,
            resource_list=[],
            listing_urls=self.listing_urls,
        )

    def list_json(self):
        # TODO: handle case when flask return 302 because token is expired
        limit = request.args.get('length')
        if limit == '-1':
            limit = None

        offset = request.args.get('start')
        direction = request.args.get('order[0][dir]')
        order_column = request.args.get('order[0][column]', 0)
        order = request.args.get(f'columns[{order_column}][data]')
        search = request.args.get('search[value]')

        result = self.service.list(
            search=search, order=order, limit=limit, direction=direction, offset=offset
        )

        return jsonify(
            {
                'recordsTotal': result['total'],
                'recordsFiltered': result.get('filtered', result['total']),
                'data': result['items'],
            }
        )


class NewViewMixin:
    listing_urls = listing_urls

    def new(self):
        return self._new()

    def _new(self, form=None):
        form = form or self.form()
        form = self._populate_form(form)

        return render_template(
            self._get_template('add'), form=form, listing_urls=self.listing_urls
        )


class BaseHelperViewWithoutLogin(FlaskView):
    form = None
    resource = None
    service = None
    templates = {}

    def _get_current_breadcrumbs(self):
        breadcrumbs = []
        names = request.args.getlist('bc_names[]')
        urls = request.args.getlist('bc_urls[]')
        icons = request.args.getlist('bc_icons[]')

        for idx, name in enumerate(names):
            breadcrumbs.append(
                {
                    'name': name,
                    'link': self._get_breadcrumb_url(idx, names, urls, icons),
                    'icon': icons[idx],
                }
            )

        return breadcrumbs

    def _get_breadcrumb_url(self, idx, names, urls, icons):
        url = urls[idx]
        first_params = True

        for i in range(0, idx):
            url += ('?' if first_params else '&') + 'bc_names[]=' + names[i]
            url += '&bc_urls[]=' + urls[i]
            url += '&bc_icons[]=' + icons[i]

            first_params = False

        return url

    def _map_form_to_resources_post(self, form):
        return self._map_form_to_resources(form)

    def _map_resources_to_form(self, resource):
        return self.form(data=resource)

    def _populate_form(self, form):
        return form

    def _map_form_to_resources(self, form, form_id=None) -> dict:
        data = form.to_dict()
        if form_id:
            try:
                data['id'] = int(form_id)
            except ValueError:
                data['uuid'] = form_id
        return data

    def _map_resources_to_form_errors(self, form, resources):
        for resource in resources.values():
            form.populate_errors(resource)
            return form

    def _get_template(self, type_):
        return self.templates.get(
            type_, DEFAULT_TEMPLATE.format(blueprint=request.blueprint, type_=type_)
        )

    def _redirect_referrer_or(self, method_view):
        if request.referrer:
            return redirect(request.referrer)

        return redirect(url_for(f'.{self.__class__.__name__}:{method_view}'))

    def _redirect_for(self, method_view):
        return redirect(url_for(f'.{self.__class__.__name__}:{method_view}'))

    def _fill_form_error(self, form, error):
        error_resources = self._extract_error_for_form(error)
        if error_resources:
            form = self._map_resources_to_form_errors(form, error_resources)
        return form

    def _flash_http_error(self, error):
        response = error.response.json()
        resource = ErrorExtractor.get_resource_from_error(error)
        generic_error = ErrorTranslator.generic_messages.get(
            response.get('error_id'), ''
        )
        flash(
            f'{resource}{": " if resource else ""}{generic_error}',
            'error',
        )
        flash(
            f'{error.request.method} {error.request.url}: {response}',
            'error_details',
        )

    def _flash_basic_form_errors(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f'{getattr(form, field).label.text} - {error}',
                    'error',
                )

    def _extract_error_for_form(self, error):
        response = error.response.json()
        if 'error_id' in response:
            if response['error_id'] == 'invalid-data':
                error_details = ErrorExtractor.extract_error_details(
                    response['details']
                )
                resource = ErrorExtractor.get_resource_from_error(error)

                return {resource: error_details}

    def _get_form_errors_msg(self, form):
        errors_msg = []
        for field, errors in form.errors.items():
            for error in errors:
                errors_msg.append(f'{getattr(form, field).label.text} - {error}')
        return errors_msg

    def _extract_error_message(self, error):
        response = error.response.json()
        if 'error_id' in response:
            if response['error_id'] == 'invalid-data':
                resource = ErrorExtractor.get_resource_from_error(error)
                return {resource: response['details']}
        else:
            return response['message']

    def _get_full_error(self, error):
        response = error.response.json()
        return f'{error.request.method} {error.request.url}: {response}'


# TODO implement this in all views that do not require all methods (CRUD)
class BaseHelperView(BaseHelperViewWithoutLogin, LoginRequiredView):
    pass


class Service(Protocol):
    def list(self, **kwargs) -> list[dict]:
        ...

    def get(self, id: Any) -> dict:
        ...

    def delete(self, id: Any) -> None:
        ...

    def update(self, resource: dict) -> dict:
        ...

    def create(self, resource: dict) -> dict:
        ...


class BaseView(BaseHelperView):
    listing_urls = listing_urls
    service: Service

    def index(self):
        return self._index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(
            self._get_template('list'),
            form=form,
            resource_list=resource_list,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    def post(self):
        form = self.form()
        resources = self._map_form_to_resources_post(form)

        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._new(form)

        try:
            self.service.create(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._new(form)

        flash(
            _('%(resource)s: Resource has been created', resource=self.resource),
            'success',
        )
        return self._redirect_referrer_or('index')

    def _new(self, form=None):
        return self._index(form)

    def get(self, id):
        return self._get(id)

    def _get(self, id, form=None):
        try:
            resource = self.service.get(id)
        except HTTPError as error:
            self._flash_http_error(error)
            return self._redirect_for('index')

        form = form or self._map_resources_to_form(resource)
        form = self._populate_form(form)

        return render_template(
            self._get_template('edit'),
            form=form,
            resource=resource,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    @route('/put/<id>', methods=['POST'])
    def put(self, id):
        form = self.form()
        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._get(id, form)

        resources = self._map_form_to_resources_put(form, id)
        try:
            self.service.update(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._get(id, form)

        flash(
            _('%(resource)s: Resource has been updated', resource=self.resource),
            'success',
        )
        return self._redirect_for('index')

    def _map_form_to_resources_put(self, form, form_id):
        return self._map_form_to_resources(form, form_id)

    @route('/delete/<id>', methods=['GET'])
    def delete(self, id):
        try:
            self.service.delete(id)
            flash(
                _(
                    '%(resource)s: Resource %(id)s has been deleted',
                    resource=self.resource,
                    id=id,
                ),
                'success',
            )
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_referrer_or('index')

    def _convert_empty_string_to_none(self, value):
        # This behavior is a bug from wtforms and is fixed in newer version
        if value == 'None':
            return None
        if not value:
            return None
        return value


def extract_select2_params(args, limit=10):
    search = args.get('term')
    page = args.get('page')

    if not _is_positive_integer(page):
        page = 1

    offset = (int(page) - 1) * limit
    return {'search': search, 'offset': offset, 'limit': limit}


def _is_positive_integer(value):
    if value is None:
        return False

    try:
        value = int(value)
    except ValueError:
        return False

    if value < 0:
        return False
    return True


def build_select2_response(results, total, params):
    return {
        'results': results,
        'pagination': {'more': (params['offset'] + params['limit']) < total},
    }
