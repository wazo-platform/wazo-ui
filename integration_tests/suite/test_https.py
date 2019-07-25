# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that
from hamcrest import contains_string
from xivo_test_helpers import until

from .helpers.base import SSLIntegrationTest


class TestHTTPSMissingCertificate(SSLIntegrationTest):
    asset = 'no_ssl_certificate'

    def test_given_no_ssl_certificate_when_ui_starts_then_ui_stops(self):
        def _is_stopped():
            status = self.service_status()
            return not status['State']['Running']

        until.true(_is_stopped, tries=10, message='wazo-ui did not stop while missing SSL certificate')

        log = self.service_logs()
        assert_that(log, contains_string("No such file or directory: '/usr/share/xivo-certs/unavailable.crt'"))


class TestHTTPSMissingPrivateKey(SSLIntegrationTest):
    asset = 'no_ssl_private_key'

    def test_given_no_ssl_private_key_when_ui_starts_then_ui_stops(self):
        def _is_stopped():
            status = self.service_status()
            return not status['State']['Running']

        until.true(_is_stopped, tries=10, message='wazo-ui did not stop while missing SSL private key')

        log = self.service_logs()
        assert_that(log, contains_string("No such file or directory: '/usr/share/xivo-certs/unavailable.key'"))
