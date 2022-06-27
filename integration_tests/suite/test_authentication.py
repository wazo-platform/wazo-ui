# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, contains_string, equal_to, not_, calling, raises
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from .helpers.base import IntegrationTest
from .helpers.constants import USERNAME_PASSWORD_ERROR


class TestLogin(IntegrationTest):

    asset = 'base'

    def setUp(self):
        self.browser.logout()

    def test_empty_login(self):
        login = self.browser.login
        login.fill_name('username', '')
        login.fill_name('password', '')

        submit = login.driver.find_element(By.ID, 'submit')
        assert_that(submit.get_attribute('class'), contains_string('disabled'))

        login.save(waiting=False)

        username = login.get_input_name('username')
        assert_that(username.has_error_class())

        password = login.get_input_name('password')
        assert_that(password.has_error_class())

    def test_invalid_login(self):
        login = self.browser.login
        login.fill_name('username', 'test')
        login.fill_name('password', 'foobar')

        submit = login.driver.find_element(By.ID, 'submit')
        assert_that(submit.get_attribute('class'), not_(contains_string('disabled')))

        login.save(waiting=False)

        username = login.get_input_name('username')
        assert_that(username.get_error().text, equal_to(USERNAME_PASSWORD_ERROR))

        password = login.get_input_name('password')
        assert_that(password.get_error().text, equal_to(USERNAME_PASSWORD_ERROR))

    def test_cannot_access_without_login(self):
        assert_that(calling(self.browser.__getattr__).with_args('index'),
                    raises(TimeoutException))
