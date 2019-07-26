# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session
from requests.exceptions import HTTPError


class ExternalAuthService:

    def __init__(self, auth_client):
        self._auth = auth_client

    def list(self):
        service_list = self._auth.external.list_(session['instance']['uuid'])
        items = []

        for service in service_list['items']:
            try:
                detail = self.get(service['type'])

                items.append(service)
            except HTTPError:
                pass

        return {'items': items}

    def get(self, type):
        service = self._auth.external.get_config(type)
        return service

    def create(self, auth_data, form):
        auth_type = auth_data['type']

        return self._auth.external.create_config(auth_type, self._parse_payload(auth_data))

    def update(self, auth_data, form):
        auth_type = auth_data['type']

        return self._auth.external.update_config(auth_type, self._parse_payload(auth_data))

    def delete(self, auth_type):
        return self._auth.external.delete_config(auth_type)

    def list_types(self):
        return ['microsoft', 'mobile', 'google']

    def _parse_payload(self, auth_data):
        auth_type = auth_data['type']
        payload = auth_data[auth_type + '_config']

        return payload
