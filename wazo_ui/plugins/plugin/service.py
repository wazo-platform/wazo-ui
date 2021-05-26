# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

import requests

logger = logging.getLogger(__name__)

PLUGIN_URL = "https://plugins.wazo.community/0.1/plugins"


class PluginService:
    def __init__(self, plugind):
        self.plugind = plugind

    def install(self, plugin):
        return self.plugind.plugins.install(
            url=plugin.get('url'),
            method=plugin['method'],
            options=plugin.get('options'),
        )

    def uninstall(self, plugin):
        if 'namespace' in plugin and 'name' in plugin:
            return self.plugind.plugins.uninstall(plugin['namespace'], plugin['name'])

    def list(self, search, namespace, installed):
        if installed is False:
            return {'items': []}

        results = []
        for plugin in self.plugind.plugins.list()['items']:
            plugin['installed_version'] = plugin['version']
            if namespace and namespace != plugin['namespace']:
                continue
            if search and search not in plugin.values():
                continue
            results.append(plugin)

        return {'items': results}

    def list_community_plugins(self):
        try:
            r = requests.get(PLUGIN_URL)
            return r.json()
        except (requests.RequestException, ValueError):
            return []
