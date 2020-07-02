# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import abc
import urllib.error
import urllib.parse
import urllib.request

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec

from .select2 import Select2


class SubmitException(Exception):
    pass


class Page(object):

    TIMEOUT = 4
    POLL_FREQUENCY = 0.2
    CONFIG = {'base_url': 'http://localhost:9296'}

    def __init__(self, driver):
        self.driver = driver

    def build_url(self, *parts, **kwargs):
        path = '/'.join(parts)
        url = "{}/{}".format(self.CONFIG['base_url'].rstrip('/'), path.lstrip('/'))
        if kwargs:
            url += "?{}".format(urllib.parse.urlencode(kwargs))
        return url

    def wait(self):
        return WebDriverWait(self.driver, self.TIMEOUT, poll_frequency=self.POLL_FREQUENCY)

    def wait_for(self, by, arg, message=None):
        condition = ec.presence_of_element_located((by, arg))
        self.wait().until(condition, message=message)

    def wait_visible(self, by, arg, message=None):
        condition = ec.visibility_of_element_located((by, arg))
        self.wait().until(condition, message=message)

    def fill(self, by, arg, value, root=None):
        root = root or self.driver
        element = root.find_element(by, arg)
        if element.tag_name == 'select':
            Select(element).select_by_visible_text(value)
        elif element.get_attribute('type') == 'checkbox':
            if element.is_selected() and value is False:
                element.click()
            elif not element.is_selected() and value is True:
                element.click()
        else:
            element.clear()
            element.send_keys(value)

    def fill_name(self, name, value, root=None):
        self.fill(By.NAME, name, value, root)

    def fill_id(self, id_, value, root=None):
        self.fill(By.ID, id_, value, root)

    def select2(self, by, arg, root=None):
        root = root or self.driver
        element = root.find_element(by, arg)
        return Select2(element, root)

    def select(self, by, arg, value, root=None):
        self.select2(by, arg, root).select(value)

    def select_name(self, name, value, root=None):
        self.select(By.NAME, name, value, root)

    def select_id(self, id_, value, root=None):
        self.select(By.ID, id_, value, root)

    def get_value(self, id_, root=None):
        root = root or self.driver
        element = root.find_element_by_id(id_)
        return element.get_attribute('value')

    def get_int_value(self, id_, root=None):
        return int(self.get_value(id_, root))

    def get_checked(self, id_, root=None):
        root = root or self.driver
        element = root.find_element_by_id(id_)
        checked = element.get_attribute('checked')
        if checked:
            return True
        return False

    def get_selected_option_value(self, id_, root=None):
        root = root or self.driver
        element = root.find_element_by_id(id_)
        return Select(element).first_selected_option.get_attribute('value')

    def get_input_name(self, name, root=None):
        root = root or self.driver
        element = root.find_element_by_name(name)
        return InputElement(element)

    def extract_errors(self):
        try:
            container = self.driver.find_element_by_class_name("alert-error")
        except NoSuchElementException:
            return ''

        return container.get_attribute('innerHTML')

    def save(self):
        btn = self.driver.find_element_by_id("submit")
        btn.click()
        self.wait_for(By.CSS_SELECTOR, '.alert')

        try:
            self.driver.find_element_by_class_name("alert-success")
        except NoSuchElementException:
            raise SubmitException(self.extract_errors())

    def is_not_savable(self):
        self.wait_for(By.XPATH,
                      '//input[@id="submit" and contains(@class, "disabled")]',
                      message='Submit is savable')
        return True

    def is_savable(self):
        self.wait_for(By.XPATH,
                      '//input[@id="submit" and not(contains(@class, "disabled"))]',
                      message='Submit is not savable')
        return True


class InputElement(WebElement):

    def __init__(self, element):
        super(InputElement, self).__init__(element.parent, element.id)

    def get_error(self):
        errors = self.parent.find_element_by_class_name('with-errors')
        try:
            return errors.find_element_by_css_selector('ul li')
        except NoSuchElementException:
            return errors

    def has_error_class(self):
        errors = self.parent.find_element_by_class_name('has-error')
        try:
            return errors.get_attribute('class')
        except NoSuchElementException:
            return errors


class ListPage(Page, metaclass=abc.ABCMeta):

    line_xpath = "//tr[td[contains(., '{name}')]]"
    edit_xpath = "{}/td[1]".format(line_xpath)
    delete_xpath = "{}/td/a[@title='Delete']".format(line_xpath)

    list_selector = (By.CSS_SELECTOR, 'tbody tr')
    form_selector = (By.CSS_SELECTOR, 'form')

    @abc.abstractproperty
    def url(self):
        return

    @abc.abstractproperty
    def form_page(self):
        return

    def go(self):
        url = self.build_url(self.url)
        self.driver.get(url)

        self.wait_for_list_table()

        return self

    def add(self):
        self.add_form()
        self.wait_for_form()
        return self.form_page(self.driver)

    def add_form(self):
        btn = self.driver.find_element_by_id('add-form')
        btn.click()

    def display_add_form(self):
        self.add_form()
        return self.driver.find_element_by_css_selector('form')

    def wait_for_form(self):
        condition = ec.presence_of_element_located(self.form_selector)
        self.wait().until(condition)

    def wait_for_list_table(self):
        condition = ec.presence_of_element_located(self.list_selector)
        self.wait().until(condition)

    def edit(self, name):
        xpath = self.edit_xpath.format(name=name)

        line = self.driver.find_element_by_xpath(xpath)
        line.click()

        btn = self.driver.find_element_by_id('edit-selected-row')
        btn.click()

        self.wait_for_form()

        return self.form_page(self.driver)

    def edit_by_id(self, id_):
        url = self.build_url(self.url, str(id_))
        self.driver.get(url)
        self.wait_for_form()
        return self.form_page(self.driver)

    def delete(self, name):
        xpath = self.delete_xpath.format(name=name)

        button = self.driver.find_element_by_xpath(xpath)
        button.click()

        condition = ec.alert_is_present()
        self.wait().until(condition)
        Alert(self.driver).accept()

        condition = ec.presence_of_element_located((By.XPATH, xpath))
        self.wait().until_not(condition)

    def delete_by_id(self, id_):
        url = self.build_url(self.url, 'delete', str(id_))
        self.driver.get(url)
        self.wait_for_list_table()

    def get_row(self, text):
        table = self.driver.find_element_by_css_selector("table tbody")
        xpath = '//tr[td[contains(., "{}")]]'.format(text)
        headers = self._extract_headers(table)
        return ListRow(table.find_element_by_xpath(xpath), headers=headers)

    def _extract_headers(self, table):
        xpath = '//tr/th'
        headers = table.find_elements_by_xpath(xpath)
        return [header.text for header in headers]

    def find_row(self, text):
        try:
            return self.get_row(text)
        except NoSuchElementException:
            return None


class ListRow(object):

    def __init__(self, row, headers):
        self.row = row
        self.headers = headers

    def extract(self, column):
        index = self.headers.index(column)
        box = self.row.find_element_by_css_selector('td:nth-child({})'.format(index + 1))
        return box.text
