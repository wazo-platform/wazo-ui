# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from mock import Mock, call

import wazo_ui.helpers.service
import wazo_ui.plugins.user.service as service

from ..service import UserService


class TestUserServiceUpdateUserLines(unittest.TestCase):

    def setUp(self):
        self.confd = Mock()
        self.auth = Mock()
        service.confd = self.confd
        wazo_ui.helpers.service.confd = self.confd
        self.service = UserService(self.confd, self.auth)
        self.confd.lines.get.return_value = {'extensions': [], 'device_id': None, 'application': None}

    def test_when_line_and_existing_line_with_same_id(self):
        line = {'id': 'line-id'}
        user = {'uuid': '1234', 'lines': [line]}
        existing_user = {'lines': [line]}

        self.service._update_user_lines(existing_user, user)

        self._assert_line_updated(line)

    def test_when_line_and_existing_line_with_same_id_and_same_extension(self):
        extension = {'id': 'extension-id', 'exten': '999', 'context': 'default'}
        line = {'id': 'line-id', 'extensions': [extension]}
        user = {'uuid': '1234', 'lines': [line]}
        existing_user = {'lines': [{'id': 'line-id'}]}
        self.confd.extensions.get.return_value = {'lines': [{}], 'exten': '999', 'context': 'default'}
        self.confd.lines.get.return_value = {'device_id': None, 'extensions': [{'id': 'extension-id'}], 'application': None}

        self.service._update_user_lines(existing_user, user)

        self._assert_line_updated(line)
        self.confd.extensions.update.assert_not_called()

    def test_when_line_and_existing_line_with_same_id_and_existing_extension_not_on_existing_line(self):
        extension1 = {'id': '', 'exten': '12', 'context': 'default'}
        line = {'id': 'line-id', 'extensions': [extension1]}
        user = {'uuid': '1234', 'lines': [line]}
        existing_user = {'lines': [{'id': 'line-id'}]}
        self.confd.lines.get.return_value = {'device_id': None, 'extensions': [], 'application': None}
        self.confd.extensions.list.return_value = {'items': [extension1]}

        self.service._update_user_lines(existing_user, user)

        self._assert_line_updated(line)
        self.confd.extensions.create.assert_not_called()
        self.confd.lines.return_value.add_extension.assert_called_once_with(extension1)

    def test_when_line_and_existing_line_with_same_id_and_extension_and_no_existing_extension(self):
        extension1 = {'id': '', 'exten': '12', 'context': 'default'}
        line = {'id': 'line-id', 'extensions': [extension1]}
        user = {'uuid': '1234', 'lines': [line]}
        existing_user = {'lines': [{'id': 'line-id'}]}
        self.confd.lines.get.return_value = {'device_id': None, 'extensions': [], 'application': None}
        self.confd.extensions.create.return_value = {'id': 'extension-id'}
        self.confd.extensions.list.return_value = {'items': []}

        self.service._update_user_lines(existing_user, user)

        self._assert_line_updated(line)
        self.confd.extensions.create.assert_called_once_with(extension1)
        self.confd.lines.return_value.add_extension.assert_called_once_with({'id': 'extension-id'})

    def test_when_line_and_existing_line_with_same_id_and_no_extension_and_existing_extension(self):
        line = {'id': 'line-id', 'extensions': []}
        user = {'uuid': '1234', 'lines': [line]}
        existing_user = {'lines': [{'id': 'line-id'}]}
        self.confd.lines.get.return_value = {'device_id': None, 'extensions': [{'id': 'extension-id'}], 'application': None}
        self.confd.extensions.create.return_value = {'id': 'extension-id'}

        self.service._update_user_lines(existing_user, user)

        self._assert_line_updated(line)
        self.confd.extensions.delete.assert_called_once_with({'id': 'extension-id'})
        self.confd.lines.return_value.remove_extension.assert_called_once_with({'id': 'extension-id'})

    def test_when_line_and_existing_line_with_same_id_and_endpoint_sip(self):
        line = {'id': 'line-id', 'endpoint_sip': {'id': 'endpoint-sip-id'}}
        user = {'uuid': '1234', 'lines': [line]}
        existing_user = {'lines': [{'id': 'line-id'}]}

        self.service._update_user_lines(existing_user, user)

        self._assert_line_updated(line)
        self.confd.endpoints_sip.update.assert_called_once_with({'id': 'endpoint-sip-id'})

    def _assert_line_updated(self, line):
        self.confd.lines.update.assert_called_once_with(line)
        self.confd.lines.create.assert_not_called()
        self.confd.lines.delete.assert_not_called()

    def test_when_line_and_no_existing_line(self):
        user = {'uuid': '1234', 'lines': [{'id': ''}]}
        existing_user = {'lines': []}
        self.confd.lines.create.return_value = new_line = {'id': 'new-line-id'}

        self.service._update_user_lines(existing_user, user)

        self.confd.lines.create.assert_called_once_with(new_line)
        self.confd.users.return_value.update_lines.assert_called_once_with([new_line])
        self.confd.lines.update.assert_not_called()
        self.confd.lines.delete.assert_not_called()

    def test_when_line_and_no_existing_line_with_id(self):
        lines = [{'id': 'line-id'}]
        user = {'uuid': '1234', 'lines': lines}
        existing_user = {'lines': []}

        self.service._update_user_lines(existing_user, user)

        for line in lines:
            self.confd.lines.update.assert_called_once_with(line)
        self.confd.users.return_value.update_lines.assert_called_once_with(lines)

    def test_when_line_and_no_existing_line_with_endpoint_sip(self):
        user = {'uuid': '1234', 'lines': [{'endpoint_sip': {}}]}
        existing_user = {'lines': []}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.endpoints_sip.create.return_value = {'id': 'new-sip-id'}

        self.service._update_user_lines(existing_user, user)

        self.confd.endpoints_sip.create.assert_called_once()
        self.confd.lines.return_value.add_endpoint_sip.assert_called_once_with({'id': 'new-sip-id'})

    def test_when_line_and_no_existing_line_with_endpoint_sccp(self):
        user = {'uuid': '1234', 'lines': [{'endpoint_sccp': {}}]}
        existing_user = {'lines': []}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.endpoints_sccp.create.return_value = {'id': 'new-sccp-id'}

        self.service._update_user_lines(existing_user, user)

        self.confd.endpoints_sccp.create.assert_called_once_with({})
        self.confd.lines.return_value.add_endpoint_sccp.assert_called_once_with({'id': 'new-sccp-id'})

    def test_when_line_and_no_existing_line_with_endpoint_custom(self):
        user = {'uuid': '1234', 'lines': [{'endpoint_custom': {}}]}
        existing_user = {'lines': []}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.endpoints_custom.create.return_value = {'id': 'new-custom-id'}

        self.service._update_user_lines(existing_user, user)

        self.confd.endpoints_custom.create.assert_called_once_with({})
        self.confd.lines.return_value.add_endpoint_custom.assert_called_once_with({'id': 'new-custom-id'})

    def test_when_line_and_no_existing_line_with_extension_and_no_existing_extension(self):
        extension = {'exten': '123', 'context': 'default'}
        user = {'uuid': '1234', 'lines': [{'endpoint_sip': {}, 'extensions': [extension]}]}
        existing_user = {'lines': []}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.extensions.create.return_value = {'id': 'new-extension-id'}
        self.confd.extensions.list.return_value = {'items': []}

        self.service._update_user_lines(existing_user, user)

        self.confd.extensions.create.assert_called_once_with(extension)
        self.confd.lines.return_value.add_extension.assert_called_once_with({'id': 'new-extension-id'})

    def test_when_line_and_no_existing_line_with_extension_and_existing_extension(self):
        extension = {'exten': '123', 'context': 'default'}
        user = {'uuid': '1234', 'lines': [{'endpoint_sip': {}, 'extensions': [extension]}]}
        existing_user = {'lines': []}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.extensions.list.return_value = {'items': [{'id': 'extension-id'}]}

        self.service._update_user_lines(existing_user, user)

        self.confd.extensions.create.assert_not_called()
        self.confd.lines.return_value.add_extension.assert_called_once_with({'id': 'extension-id'})

    def test_when_line_and_no_existing_line_with_device_id(self):
        user = {'uuid': '1234', 'lines': [{'endpoint_sip': {}, 'device_id': 'device-id'}]}
        existing_user = {'lines': []}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}

        self.service._update_user_lines(existing_user, user)

        self.confd.lines.return_value.add_device.assert_called_once_with('device-id')

    def test_when_line_and_no_existing_line_with_application_uuid(self):
        application = {'uuid': 'app-uuid'}
        user = {'uuid': '1234', 'lines': [{'endpoint_sip': {}, 'application': application}]}
        existing_user = {'lines': []}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}

        self.service._update_user_lines(existing_user, user)

        self.confd.lines.return_value.add_application.assert_called_once_with(application)

    def test_when_no_line_and_no_existing_line(self):
        user = {'uuid': '1234', 'lines': []}
        existing_user = {'lines': []}

        self.service._update_user_lines(existing_user, user)

        self.confd.lines.update.assert_not_called()
        self.confd.lines.create.assert_not_called()
        self.confd.lines.delete.assert_not_called()

    def test_when_no_line_and_existing_line(self):
        user = {'uuid': '1234', 'lines': []}
        existing_user = {'lines': [{'id': 'line-id'}]}
        self.confd.lines.get.return_value = {'device_id': 'device-id'}

        self.service._update_user_lines(existing_user, user)

        self._assert_line_deleted('line-id')
        self.confd.lines.return_value.remove_device.assert_called_once_with('device-id')

    def _assert_line_deleted(self, line):
        self.confd.lines.delete.assert_called_once_with(line)
        self.confd.lines.create.assert_not_called()
        self.confd.lines.update.assert_not_called()

    def test_when_swapping_lines(self):
        line1 = {'id': 'line1-id'}
        line2 = {'id': 'line2-id'}
        user = {'uuid': '1234', 'lines': [line2, line1]}
        existing_user = {'lines': [line1, line2]}

        self.service._update_user_lines(existing_user, user)

        self.confd.lines.update.assert_has_calls([call(line2), call(line1)])
        self.confd.users.return_value.update_lines.called_once_with([line2, line1])
        self.confd.lines.delete.assert_not_called()

    def test_when_extension_is_updated_and_it_is_associated_with_other_lines(self):
        form_extension = {'id': 'extension-id', 'exten': '123', 'context': 'default'}
        old_extension = {'id': 'extension-id', 'exten': '234', 'context': 'default', 'lines': [{}, {}]}
        form_line = {'id': 'line1-id', 'extensions': [form_extension]}
        old_line = {'id': 'line1-id', 'extensions': [old_extension]}
        form_user = {'uuid': '1234', 'lines': [form_line]}
        old_user = {'uuid': '1234', 'lines': [old_line]}
        self.confd.extensions.get.return_value = old_extension
        self.confd.extensions.list.return_value = {'items': []}
        self.confd.extensions.create.return_value = form_extension

        self.service._update_user_lines(old_user, form_user)

        self.confd.lines.update.assert_called_once_with(form_line)
        self.confd.lines.return_value.remove_extension.assert_called_once_with(old_extension)
        self.confd.extensions.create.assert_called_once_with(form_extension)
        self.confd.lines.return_value.add_extension.assert_called_once_with(form_extension)
        self.confd.lines.delete.assert_not_called()
        self.confd.extensions.delete.assert_not_called()

    def test_when_extension_is_not_updated_and_it_is_associated_with_other_lines(self):
        extension = {'id': 'extension-id', 'exten': '123', 'context': 'default'}
        line = {'id': 'line1-id', 'extensions': [extension]}
        user = {'uuid': '1234', 'lines': [line]}
        existing_user = {'lines': [line]}
        self.confd.extensions.get.return_value = {'lines': [{}, {}], 'exten': '123', 'context': 'default'}
        self.confd.extensions.create.return_value = extension

        self.service._update_user_lines(existing_user, user)

        self.confd.lines.update.assert_called_once_with(line)
        self.confd.extensions.update.assert_not_called()
        self.confd.lines.return_value.remove_extension.assert_not_called()
        self.confd.lines.return_value.add_extension.assert_not_called()
        self.confd.lines.delete.assert_not_called()
        self.confd.extensions.create.assert_not_called()
        self.confd.extensions.delete.assert_not_called()


class TestUserServiceCreateUserLines(unittest.TestCase):

    def setUp(self):
        self.confd = Mock()
        self.auth = Mock()
        service.confd = self.confd
        wazo_ui.helpers.service.confd = self.confd
        self.service = UserService(self.confd, self.auth)
        self.confd.lines.get.return_value = {'extensions': []}

    def test_when_line_with_no_id(self):
        user = {'uuid': '1234', 'lines': [{'id': ''}]}
        self.confd.lines.create.return_value = new_line = {'id': 'new-line-id'}

        self.service._create_user_lines(user)

        self.confd.lines.create.assert_called_once_with(new_line)
        self.confd.users.return_value.add_line.assert_called_once_with(new_line)
        self.confd.lines.update.assert_not_called()
        self.confd.lines.delete.assert_not_called()

    def test_when_line_with_id(self):
        line = {'id': 'line-id'}
        user = {'uuid': '1234', 'lines': [line]}

        self.service._create_user_lines(user)

        self.confd.users.return_value.add_line.assert_called_once_with(line)

    def test_when_line_with_endpoint_sip(self):
        user = {'uuid': '1234', 'lines': [{'endpoint_sip': {}}]}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.endpoints_sip.create.return_value = {'id': 'new-sip-id'}

        self.service._create_user_lines(user)

        self.confd.endpoints_sip.create.assert_called_once()
        self.confd.lines.return_value.add_endpoint_sip.assert_called_once_with({'id': 'new-sip-id'})

    def test_when_line_with_endpoint_sccp(self):
        user = {'uuid': '1234', 'lines': [{'endpoint_sccp': {}}]}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.endpoints_sccp.create.return_value = {'id': 'new-sccp-id'}

        self.service._create_user_lines(user)

        self.confd.endpoints_sccp.create.assert_called_once_with({})
        self.confd.lines.return_value.add_endpoint_sccp.assert_called_once_with({'id': 'new-sccp-id'})

    def test_when_line_with_endpoint_custom(self):
        user = {'uuid': '1234', 'lines': [{'endpoint_custom': {}}]}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.endpoints_custom.create.return_value = {'id': 'new-custom-id'}

        self.service._create_user_lines(user)

        self.confd.endpoints_custom.create.assert_called_once_with({})
        self.confd.lines.return_value.add_endpoint_custom.assert_called_once_with({'id': 'new-custom-id'})

    def test_when_line_with_extension_and_no_existing_extension(self):
        extension = {'exten': '123', 'context': 'default'}
        user = {'uuid': '1234', 'lines': [{'endpoint_sip': {}, 'extensions': [extension]}]}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.extensions.create.return_value = {'id': 'new-extension-id'}
        self.confd.extensions.list.return_value = {'items': []}

        self.service._create_user_lines(user)

        self.confd.extensions.create.assert_called_once_with(extension)
        self.confd.lines.return_value.add_extension.assert_called_once_with({'id': 'new-extension-id'})

    def test_when_line_with_extension_and_existing_extension(self):
        extension = {'exten': '123', 'context': 'default'}
        user = {'uuid': '1234', 'lines': [{'endpoint_sip': {}, 'extensions': [extension]}]}
        self.confd.lines.create.return_value = {'id': 'new-line-id'}
        self.confd.extensions.list.return_value = {'items': [{'id': 'extension-id'}]}

        self.service._create_user_lines(user)

        self.confd.extensions.create.assert_not_called()
        self.confd.lines.return_value.add_extension.assert_called_once_with({'id': 'extension-id'})


class TestUserServiceUpdateDeviceAssociation(unittest.TestCase):

    def setUp(self):
        self.confd = Mock()
        self.auth = Mock()
        service.confd = self.confd
        wazo_ui.helpers.service.confd = self.confd
        self.service = UserService(self.confd, self.auth)
        self.confd.lines.get.return_value = {'device_id': None}

    def test_when_device_and_existing_device_with_same_id(self):
        device_id = 'device-id'
        self.confd.lines.get.return_value = {'device_id': device_id}

        self.service._update_device_association('line-id', device_id)

        self.confd.lines.return_value.add_device.assert_not_called()
        self.confd.lines.return_value.remove_device.assert_not_called()

    def test_when_no_device_and_no_existing_device(self):
        device_id = ''
        self.confd.lines.get.return_value = {'device_id': None}

        self.service._update_device_association('line-id', device_id)

        self.confd.lines.return_value.add_device.assert_not_called()
        self.confd.lines.return_value.remove_device.assert_not_called()

    def test_when_no_device_and_existing_device(self):
        device_id = None
        self.confd.lines.get.return_value = {'device_id': 'device-id'}

        self.service._update_device_association('line-id', device_id)

        self.confd.lines.return_value.add_device.assert_not_called()
        self.confd.lines.return_value.remove_device.assert_called_once_with('device-id')

    def test_when_device_and_no_existing_device(self):
        device_id = 'device-id'
        self.confd.lines.get.return_value = {'device_id': None}

        self.service._update_device_association('line-id', device_id)

        self.confd.lines.return_value.add_device.assert_called_once_with('device-id')
        self.confd.lines.return_value.remove_device.assert_not_called()

    def test_when_device_and_existing_device_with_different_id(self):
        device_id = 'device1-id'
        self.confd.lines.get.return_value = {'device_id': 'device2-id'}

        self.service._update_device_association('line-id', device_id)

        self.confd.lines.return_value.remove_device.assert_called_once_with('device2-id')
        self.confd.lines.return_value.add_device.assert_called_once_with('device1-id')
