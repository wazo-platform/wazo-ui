# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase
from unittest.mock import Mock

from hamcrest import assert_that, contains_inanyorder, empty

from ..service import CallPermissionService


class TestUpdate(TestCase):
    def setUp(self):
        self.confd = Mock()
        self.service = CallPermissionService(self.confd)

    def test_find_add_and_remove(self):
        existing = [1, 2, 3]
        new = [3, 4, 5]

        add, remove = self.service.find_add_and_remove(new, existing)

        assert_that(add, contains_inanyorder(4, 5))
        assert_that(remove, contains_inanyorder(1, 2))

        existing = [1, 2, 3]
        new = None

        add, remove = self.service.find_add_and_remove(new, existing)

        assert_that(add, empty())
        assert_that(remove, contains_inanyorder(1, 2, 3))

        existing = None
        new = [3, 4, 5]

        add, remove = self.service.find_add_and_remove(new, existing)

        assert_that(add, contains_inanyorder(3, 4, 5))
        assert_that(remove, empty())

        existing = None
        new = None

        add, remove = self.service.find_add_and_remove(new, existing)

        assert_that(add, empty())
        assert_that(remove, empty())
