# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import redirect, url_for, render_template
from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import DirdProfileForm

service_names = ['favorites', 'reverse', 'lookup']


class DirdProfileView(BaseIPBXHelperView):
    form = DirdProfileForm
    resource = 'dird_profile'

    @menu_item('.ipbx.dird', l_('Directory'), icon="address-book", multi_tenant=True)
    @menu_item('.ipbx.dird.profile', l_('Profile'), icon='user', multi_tenant=True)
    def index(self):
        return super().index()

    def _get(self, id, form=None):
        try:
            resource = self.service.get(id)
            sources = self.source_service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('index.IndexView:index'))

        form = form or self._map_resources_to_form(resource)
        form = self._populate_form(form)

        for service in form.services:
            service.uuid.choices = [
                (source['uuid'], source['name']) for source in sources['items']
            ]

        return render_template(
            self._get_template('edit'),
            form=form,
            resource=resource,
            current_breadcrumbs=self._get_current_breadcrumbs(),
            listing_urls=self.listing_urls,
        )

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        services = {
            'favorites': {'sources': []},
            'reverse': {'sources': []},
            'lookup': {'sources': []},
        }

        for service in resource['services']:
            for service_name in service_names:
                if service_name in service and service[service_name]:
                    services[service_name]['sources'].append({'uuid': service['uuid']})

        resource = self.service.get(resource['uuid'])
        resource['services'] = services

        return resource

    def _map_resources_to_form(self, resource):
        services_by_uuid = {}
        services = resource['services']
        sources = (
            services['favorites']['sources']
            + services['reverse']['sources']
            + services['lookup']['sources']
        )

        # Initialize all services to False for each sources
        for source in sources:
            if not source['uuid'] in services_by_uuid:
                services_by_uuid[source['uuid']] = {
                    service_name: False for service_name in service_names
                }

        # Set source enabled for each service
        for service_name in service_names:
            for source in resource['services'][service_name]['sources']:
                services_by_uuid[source['uuid']][service_name] = True

        resource['services'] = []
        for uuid, services in services_by_uuid.items():
            service = {'uuid': uuid}
            service.update(services)
            resource['services'].append(service)

        form = self.form(data=resource)
        return form
