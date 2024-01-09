# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from hamcrest import assert_that, equal_to
from unittest.mock import Mock

from wazo_ui.helpers.service import BaseConfdService
from wazo_ui.helpers.extension import BaseConfdExtensionService


class TestBaseConfdService(unittest.TestCase):
    def setUp(self):
        self.confd = Mock()
        self.service = BaseConfdService()
        self.service._confd = self.confd
        self.service.resource_confd = 'resource1'

    def test_list(self):
        self.confd.resource1.list.return_value = [{'name': 'value'}]
        result = self.service.list()
        assert_that(result, equal_to([{'name': 'value'}]))

    def test_get(self):
        self.confd.resource1.get.return_value = {'name': 'value'}
        result = self.service.get(42)
        assert_that(result, equal_to({'name': 'value'}))

    def test_update(self):
        resource = {'name': 'value2'}
        self.service.update(resource)
        self.confd.resource1.update.assert_called_once_with({'name': 'value2'})

    def test_create(self):
        resource = {'name': 'value2'}
        self.service.create(resource)
        self.confd.resource1.create.assert_called_once_with({'name': 'value2'})

    def test_delete(self):
        self.service.delete(42)
        self.confd.resource1.delete.assert_called_once_with(42)


class TestBaseConfdExtensionService(unittest.TestCase):
    def setUp(self):
        self.confd = Mock()
        self.service = BaseConfdExtensionService()
        self.service._confd = self.confd
        self.service.resource_confd = 'resource1'

    def _assert_no_confd_call(self):
        self.confd.extensions.create.assert_not_called()
        self.confd.extensions.update.assert_not_called()
        self.confd.extensions.delete.assert_not_called()
        self.confd.resource1.assert_not_called()
        self.confd.resource1.return_value.remove_extension.assert_not_called()
        self.confd.resource1.return_value.add_extension.assert_not_called()

    def test_update_extension_when_no_extension(self):
        resource = {'id': 3}
        extension = None
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_no_resource(self):
        resource = {'id': 3}
        extension = None
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_extension_is_empty(self):
        resource = {'id': 3}
        extension = {}
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_exten_is_removed(self):
        existing_extension = {'exten': None, 'context': 'default', 'id': 42}
        self.confd.resource1.get.return_value = {'extensions': [existing_extension]}
        resource = {'id': 3}
        extension = {'exten': None, 'context': 'default'}
        self.service.update_extension(extension, resource)

        self.confd.extensions.delete.assert_called_once_with(existing_extension)
        self.confd.resource1.assert_called_once_with(resource)
        self.confd.resource1.return_value.remove_extension.assert_called_once_with(
            existing_extension
        )

    def test_update_extension_when_no_exten_key(self):
        existing_extension = {'exten': None, 'context': 'default', 'id': 42}
        self.confd.resource1.get.return_value = {'extensions': [existing_extension]}
        resource = {'id': 3}
        extension = {'context': 'default'}
        self.service.update_extension(extension, resource)

        self.confd.extensions.delete.assert_called_once_with(existing_extension)
        self.confd.resource1.assert_called_once_with(resource)
        self.confd.resource1.return_value.remove_extension.assert_called_once_with(
            existing_extension
        )

    def test_update_extension_when_no_exten_and_no_existing_extension(self):
        self.confd.resource1.get.return_value = {'extensions': []}
        resource = {'id': 3}
        extension = {'exten': None, 'context': 'default'}
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_same_extension_and_existing_extension(self):
        exten, context = '123', 'default'
        existing_extension = {'exten': exten, 'context': context, 'id': 42}
        self.confd.resource1.get.return_value = {'extensions': [existing_extension]}
        resource = {'id': 3}
        extension = {'exten': exten, 'context': context}
        self.service.update_extension(extension, resource)
        self._assert_no_confd_call()

    def test_update_extension_when_different_extension_and_existing_extension(self):
        existing_extension = {'exten': '123', 'context': 'default', 'id': 42}
        self.confd.resource1.get.return_value = {'extensions': [existing_extension]}
        resource = {'id': 3}
        extension = {'exten': '456', 'context': 'default'}
        self.service.update_extension(extension, resource)

        expected_call = extension
        expected_call['id'] = 42
        self.confd.extensions.update.assert_called_once_with(expected_call)

    def test_update_extension_when_extension_and_no_existing_extension(self):
        self.confd.resource1.get.return_value = {'extensions': []}
        resource = {'id': 3}
        extension = {'exten': '456', 'context': 'default'}
        self.confd.extensions.create.return_value = extension

        self.service.update_extension(extension, resource)

        self.confd.extensions.create.assert_called_once_with(extension)
        self.confd.resource1.assert_called_once_with(resource)
        self.confd.resource1.return_value.add_extension.assert_called_once_with(
            extension
        )

    def test_create_extension_when_no_extension(self):
        resource = {'id': 3}
        extension = None
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_no_resource(self):
        resource = {'id': 3}
        extension = None
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_extension_is_empty(self):
        resource = {'id': 3}
        extension = {}
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_exten_is_None(self):
        resource = {'id': 3}
        extension = {'exten': None, 'context': 'default'}
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_context_is_None(self):
        resource = {'id': 3}
        extension = {'exten': '123', 'context': None}
        self.service.create_extension(extension, resource)
        self._assert_no_confd_call()

    def test_create_extension_when_extension_and_resource(self):
        resource = {'id': 3}
        extension = {'exten': '1234', 'context': 'default'}
        self.confd.extensions.create.return_value = extension

        self.service.create_extension(extension, resource)

        self.confd.extensions.create.assert_called_once_with(extension)
        self.confd.resource1.assert_called_once_with(resource)
        self.confd.resource1.return_value.add_extension.assert_called_once_with(
            extension
        )

    def test_delete_extension_when_no_extension(self):
        resource = {'id': 42, 'extensions': []}
        self.confd.resource1.get.return_value = resource
        self.service.delete_extension(resource['id'])
        self._assert_no_confd_call()

    def test_delete_extension_when_extension_and_resource(self):
        extension = {'id': 1, 'exten': '1234', 'context': 'default'}
        resource = {'id': 42, 'extensions': [extension]}
        self.confd.resource1.get.return_value = resource

        self.service.delete_extension(resource['id'])

        self.confd.extensions.delete.assert_called_once_with(extension)
        self.confd.resource1.assert_called_once_with(resource)
        self.confd.resource1.return_value.remove_extension.assert_called_once_with(
            extension
        )
