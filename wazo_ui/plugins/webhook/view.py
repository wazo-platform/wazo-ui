# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import pprint

from flask import redirect, render_template, url_for
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import WebhookFormHTTP


class WebhookView(BaseIPBXHelperView):
    form = WebhookFormHTTP
    resource = 'webhook'
    raw_events = []

    @menu_item(
        '.ipbx.services.webhooks', l_('Webhooks'), icon="globe", multi_tenant=True
    )
    def index(self):
        return super().index()

    def get_logs(self, id):
        try:
            resource_list = self.service.get_logs(id)
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))
        for item in resource_list["items"]:
            item["detail"] = pprint.pformat(item["detail"], width=160, indent=2)
            item["event"] = pprint.pformat(item["event"], width=80, indent=2)
        return render_template(
            self._get_template('logs'),
            resource=self.service.get(id),
            resource_list=resource_list,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    def _populate_form(self, form):
        users_by_id = {
            user['uuid']: str(user['firstname']) + ' ' + str(user['lastname'])
            for user in self.service.list_users()['items']
        }

        form.events.choices = [(event, event) for event in self.raw_events]
        form.services.choices = self._build_choices_services()
        form.user_uuid.choices = self._build_setted_choices_users(
            form.events_user_uuid, users_by_id
        )
        return form

    def _map_resources_to_form(self, resource):
        self.raw_events = resource['events']

        resource['events'] = resource.get('events')
        resource['services'] = resource.get('service')

        resource['url'] = resource['config'].get('url')
        resource['body'] = resource['config'].get('body')
        resource['verify_certificate'] = resource['config'].get('verify_certificate')
        resource['method'] = resource['config'].get('method')
        resource['content_type'] = resource['config'].get('content_type')

        form = self.form(data=resource)
        return form

    def _build_choices_services(self):
        services = self.service.list_services()
        services_list = [((''), ('Choose a service'))]
        for service in services['services']:
            services_list.append((service, service))
        return services_list

    def _build_setted_choices_users(self, user_uuid, users_by_id):
        if not user_uuid.data or user_uuid.data == 'None':
            return []
        return [(user_uuid.data, users_by_id[user_uuid.data])]
