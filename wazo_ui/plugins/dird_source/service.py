# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
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

    def get(self, source_uuid):
        results = [source for source in self.list()['items'] if source['uuid'] == source_uuid]
        source = results[0] if len(results) else None
        backend = source['backend']

        if backend == 'office365' or backend == 'google':
            result = self._dird.backends.get_source(backend, source_uuid)
        else:
            result = getattr(self._dird, endpoints[backend]).get(source_uuid)

        result.update(source)
        return result

    def create(self, source_data):
        backend = source_data['backend']
        source_data[backend + '_config']['name'] = source_data['name']

        if backend == 'office365' or backend == 'google':
            return self._dird.backends.create_source(backend, source_data[backend + '_config'])

        getattr(self._dird, endpoints[backend]).create(source_data[backend + '_config'])

    def update(self, source_data):
        backend = source_data['backend']
        source_data[backend + '_config']['name'] = source_data['name']

        if backend == 'office365' or backend == 'google':
            return self._dird.backends.edit_source(backend, source_data['uuid'], source_data[backend + '_config'])

        return getattr(self._dird, endpoints[backend]).edit(source_data['uuid'], source_data[backend + '_config'])

    def delete(self, source_uuid):
        source = self.get(source_uuid)
        backend = source['backend']

        if backend == 'office365' or backend == 'google':
            return self._dird.backends.delete_source(backend, source_uuid)

        getattr(self._dird, endpoints[source['backend']]).delete(source_uuid)

    def list_backends(self):
        return self._dird.backends.list()
