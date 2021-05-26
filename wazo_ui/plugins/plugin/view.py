# Copyright 2017-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import flash, jsonify, render_template, request
from flask_babel import lazy_gettext as l_
from flask_classful import route
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import LoginRequiredView
from wazo_ui.helpers.menu import menu_item


class PluginView(LoginRequiredView):
    @menu_item(
        '.ipbx.global_settings.plugins', l_('Plugins'), icon="cubes", multi_tenant=False
    )
    def index(self):
        plugins = self.service.list_community_plugins()
        return render_template('wazo_engine/plugin/list.html', plugins=plugins)

    @route('/install_plugin/', methods=['POST'])
    def install_plugin(self):
        body = request.get_json()
        plugin = self.service.install(body)
        return jsonify(plugin)

    @route('/remove_plugin/', methods=['POST'])
    def remove_plugin(self):
        body = request.get_json()
        plugin = self.service.uninstall(body)
        return jsonify(plugin)

    @route('/search_plugin/', methods=['POST'])
    def search_plugin(self):
        payload = request.get_json()
        search = payload.get('search')
        namespace = payload.get('namespace')
        installed = payload.get('installed')
        try:
            installed_plugins = self.service.list(
                search=search, namespace=namespace, installed=installed
            )['items']
            return render_template('plugin/list_plugins.html', market=installed_plugins)
        except HTTPError as error:
            flash(error, category='error')
            return render_template('flashed_messages.html')

    @route('/search_plugin_community/', methods=['POST'])
    def search_plugin_community(self):
        return ""
