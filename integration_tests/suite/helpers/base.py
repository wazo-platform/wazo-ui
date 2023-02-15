# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_test_helpers.asset_launching_test_case import AssetLaunchingTestCase

from .asset_launching_test_case import AdminUIAssetLaunchingTestCase
from .constants import ASSET_ROOT
from .pages.index import IndexPage


class SSLIntegrationTest(AssetLaunchingTestCase):
    assets_root = ASSET_ROOT
    service = 'ui'


class IntegrationTest(AdminUIAssetLaunchingTestCase):
    assets_root = ASSET_ROOT

    @classmethod
    def setup_browser(cls):
        browser = super(IntegrationTest, cls).setup_browser()
        browser.pages['index'] = IndexPage
        return browser
