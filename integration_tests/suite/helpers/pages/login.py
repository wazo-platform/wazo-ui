# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .page import Page


class LoginPage(Page):

    PATH = "/login"

    def login(self, username, password, language='en'):
        self.go()
        self.fill_name('username', username)
        self.fill_name('password', password)
        self.select_name('language', language)
        self.save()

    def logout(self):
        try:
            user_menu = self.driver.find_element(By.CLASS_NAME, 'user-menu')
            user_menu.click()
            self.wait_for(By.ID, 'logout')
            btn = self.driver.find_element(By.ID, 'logout')
        except NoSuchElementException:
            return
        btn.click()
        self.wait_for(By.NAME, 'username')

    def go(self):
        url = self.build_url(self.PATH)
        self.driver.get(url)
        self.wait_for(By.NAME, 'username')
        return self

    def save(self, waiting=True):
        btn = self.driver.find_element(By.ID, "submit")
        btn.click()
        if waiting:
            self.wait_for(By.CLASS_NAME, 'wazo-logo')
        else:
            self.wait_for(By.NAME, 'username')

    def select_name(self, name, value):
        element = self.driver.find_element(By.NAME, name)
        Select(element).select_by_value(value)
