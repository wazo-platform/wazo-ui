# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

endpoints = {
    'conference': 'conference_source',
    'csv': 'csv_source',
    'csv_ws': 'csv_ws_source',
    'ldap': 'ldap_source',
    'personal': 'personal_source',
    'phonebook': 'phonebook_source',
    'wazo': 'wazo_source',
}


class DirdSourceService:
    def __init__(self, dird_client):
        self._dird = dird_client

    def list(self):
        return self._dird.sources.list()

    def get(self, backend, source_uuid):
        if backend not in endpoints.keys():
            result = self._dird.backends.get_source(backend, source_uuid)
        else:
            result = getattr(self._dird, endpoints[backend]).get(source_uuid)

        result['backend'] = backend
        return result

    def create(self, source_data):
        backend = source_data['backend']
        source_data[backend + '_config']['name'] = source_data['name']

        if backend not in endpoints.keys():
            return self._dird.backends.create_source(
                backend, source_data[backend + '_config']
            )

        getattr(self._dird, endpoints[backend]).create(source_data[backend + '_config'])

    def update(self, source_data):
        backend = source_data['backend']
        source_data[backend + '_config']['name'] = source_data['name']

        if backend not in endpoints.keys():
            return self._dird.backends.edit_source(
                backend, source_data['uuid'], source_data[backend + '_config']
            )

        return getattr(self._dird, endpoints[backend]).edit(
            source_data['uuid'], source_data[backend + '_config']
        )

    def delete(self, backend, source_uuid):
        if backend not in endpoints.keys():
            return self._dird.backends.delete_source(backend, source_uuid)

        getattr(self._dird, endpoints[backend]).delete(source_uuid)

    def list_backends(self):
        return self._dird.backends.list()

    def get_phonebook(self, phonebook_uuid):
        return self._dird.phonebook.get(phonebook_uuid=phonebook_uuid)
