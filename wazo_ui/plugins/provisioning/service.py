# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_ui.helpers.service import BaseConfdService
from wazo_provd_client.operation import OperationInProgress


class PluginService:

    def __init__(self, provd_client):
        self._provd = provd_client

    def list_installed(self, search=None, **kwargs):
        plugins_installed = self._provd.plugins.list_installed(**kwargs)['pkgs']
        if search:
            plugins_installed = self._filter_dict(plugins_installed, search)
        return self._prepare_resource_list_for_view(plugins_installed)

    def list_installable(self, search=None, **kwargs):
        plugins_installable = self._provd.plugins.list_installable(**kwargs)['pkgs']
        if search:
            plugins_installable = self._filter_dict(plugins_installable, search)
        return self._prepare_resource_list_for_view(plugins_installable)

    def get(self, id):
        return self._provd.plugins.get(id)

    def update(self):
        self._provd.plugins.update()

    def install(self, id):
        self._provd.plugins.install(id)

    def uninstall(self, id):
        self._provd.plugins.uninstall(id)

    def get_packages_installed(self, plugin, **kwargs):
        packages_installed = self._provd.plugins.get_packages_installed(plugin=plugin, **kwargs)['pkgs']
        return self._prepare_resource_list_for_view(packages_installed)

    def get_packages_installable(self, plugin, **kwargs):
        packages_installable = self._provd.plugins.get_packages_installable(plugin=plugin, **kwargs)['pkgs']
        return self._prepare_resource_list_for_view(packages_installable)

    def install_package(self, plugin_name, package_name):
        return self._provd.plugins.install_package(plugin_name, package_name)

    def get_package_status(self, location):
        return OperationInProgress(self._provd.plugins, location=location)

    def uninstall_package(self, plugin_name, package_name):
        return self._provd.plugins.uninstall_package(plugin_name, package_name)

    def _prepare_resource_list_for_view(self, resource_list):
        for plugin_name, plugin_infos in resource_list.items():
            plugin_infos.update({
                'id': plugin_name,
                'name': plugin_name
            })
            if 'dsize' in plugin_infos:
                plugin_infos['dsize'] = self._format_bytes_to_human_readable_size(plugin_infos['dsize'])

        result = {
            'items': list(resource_list.values()),
            'total': len(resource_list)
        }
        return result

    def _format_bytes_to_human_readable_size(self, size):
        for count in ['Bytes', 'KB', 'MB', 'GB']:
            if size > -1024.0 and size < 1024.0:
                return "%3.1f%s" % (size, count)
            size /= 1024.0
        return "%3.1f%s" % (size, 'TB')

    def _filter_dict(self, dict_, search):
        return {key: value for key, value in dict_.items() if search in key}


class ConfigService:

    def __init__(self, provd_client):
        self._provd = provd_client

    def get(self, id):
        return self._provd.configs.get(id)

    def create(self, resource):
        return self._provd.configs.create(resource)

    def update(self, resource):
        self._provd.configs.update(resource)

    def delete(self, id):
        self._provd.configs.delete(id)

    def autocreate(self):
        self._provd.configs.autocreate()

    def list_device(self, **kwargs):
        configs_device = self._provd.configs.list_device(**kwargs)
        return self._prepare_resource_list_for_view(configs_device['configs'])

    def _prepare_resource_list_for_view(self, resource_list):
        result = {
            'items': resource_list,
            'total': len(resource_list)
        }
        return result


class RegistrarService(BaseConfdService):

    resource_confd = 'registrars'

    def __init__(self, confd_client):
        self._confd = confd_client


class ConfigurationService(object):

    def __init__(self, provd_client, confd_client):
        self._provd = provd_client
        self._confd = confd_client

    def update(self, resource):
        for param in resource['general_config']:
            self._provd.params.update(param, resource['general_config'][param])
        self._confd.provisioning_networking.update(resource['network_config'])

    def get(self):
        resource = {}
        config = self._provd.params.list()['params']
        resource['general_config'] = self._prepare_for_view(config)
        resource['network_config'] = self._confd.provisioning_networking.get()

        return resource

    def _prepare_for_view(self, configs):
        data = {}
        for setting in configs:
            data[setting['id']] = setting['value']
        return data
