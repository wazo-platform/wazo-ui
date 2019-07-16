# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from easyprocess import log as easyprocess_logger
from pyvirtualdisplay import Display

from .login import LoginPage

easyprocess_logger.setLevel(logging.CRITICAL)
LOGGER.setLevel(logging.CRITICAL)


class Browser(object):

    pages = {'login': LoginPage}

    def __init__(self, username, password, virtual=True):
        self.username = username
        self.password = password
        self.display = Display(visible=virtual, size=(1920, 1080))

    def start(self):
        self.display.start()
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
        self._login()

    def _login(self):
        LoginPage(self.driver).login(self.username, self.password)

    def logout(self):
        LoginPage(self.driver).logout()

    def __getattr__(self, name):
        page = self.pages[name](self.driver)
        return page.go()

    def stop(self):
        self.driver.close()
        self.display.stop()


class RemoteBrowser(Browser):

    def __init__(self, remote_url, username, password):
        self.remote_url = remote_url
        self.username = username
        self.password = password

    def start(self):
        self.driver = webdriver.Remote(command_executor=self.remote_url, desired_capabilities=DesiredCapabilities.FIREFOX)
        self.driver.set_window_size(1920, 1080)
        self._login()

    def stop(self):
        self.driver.close()
