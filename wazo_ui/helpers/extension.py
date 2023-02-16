# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from xivo.xivo_helpers import clean_extension

from .service import BaseConfdService

logger = logging.getLogger(__name__)

__all__ = [
    'clean_extension',
]


class BaseConfdExtensionService(BaseConfdService):
    def _extract_main_extension(self, resource):
        extensions = resource.get('extensions')
        for extension in extensions:
            return extension
        logger.debug('Missing extension resource')

    def create(self, resource):
        resource_created = super().create(resource)
        extension = self._extract_main_extension(resource)
        self.create_extension(extension, resource_created)
        return resource_created

    def update(self, resource):
        super().update(resource)
        extension = self._extract_main_extension(resource)
        self.update_extension(extension, resource)

    def delete(self, resource_id):
        self.delete_extension(resource_id)
        super().delete(resource_id)

    def create_extension(self, extension, resource):
        if resource and extension:
            if extension.get('exten') and extension.get('context'):
                self._add_extension(extension, resource)

    def update_extension(self, extension, resource):
        if not extension or not resource:
            return

        existing_extension = self._get_main_extension(resource)

        if extension.get('exten') and existing_extension:
            self._update_extension(extension, existing_extension)

        elif extension.get('exten'):
            self._add_extension(extension, resource)

        elif not extension.get('exten') and existing_extension:
            self._remove_extension(existing_extension, resource)

    def delete_extension(self, resource_id):
        resource_client = getattr(self._confd, self.resource_confd)
        resource = resource_client.get(resource_id)
        for extension in resource['extensions']:
            self._remove_extension(extension, resource)

    def _add_extension(self, extension, resource):
        extension = self._confd.extensions.create(extension)
        if extension:
            resource_client = getattr(self._confd, self.resource_confd)
            resource_client(resource).add_extension(extension)

    def _update_extension(self, extension, existing_extension):
        if existing_extension.get('exten') == extension.get(
            'exten'
        ) and existing_extension.get('context') == extension.get('context'):
            return

        extension['id'] = existing_extension['id']
        self._confd.extensions.update(extension)

    def _remove_extension(self, extension, resource):
        resource_client = getattr(self._confd, self.resource_confd)
        resource_client(resource).remove_extension(extension)
        self._confd.extensions.delete(extension)

    def _get_main_extension(self, resource):
        resource_id = resource.get('uuid', resource.get('id'))
        if not resource_id:
            logger.debug(
                'Unable to extract resource_id from %s resource', self.resource_confd
            )
            return

        resource_client = getattr(self._confd, self.resource_confd)
        for extension in resource_client.get(resource_id)['extensions']:
            return extension
        return None
