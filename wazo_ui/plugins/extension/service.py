# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class ExtensionService(BaseConfdService):
    resource_confd = 'extensions'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_context(self, context):
        contexts = self._confd.contexts.list(name=context)['items']
        for context in contexts:
            return context
        return None


class ExtensionFeaturesService(BaseConfdService):
    resource_confd = 'extensions_features'

    def __init__(self, confd_client):
        self._confd = confd_client

    def update_extension_features(self, resources):
        existing_resources = self._confd.extensions_features.list()['items']
        for resource in resources:
            if self._feature_has_changed(existing_resources, resource):
                self.update(resource)

    def _feature_has_changed(self, existing_features, feature):
        for existing_feature in existing_features:
            if feature['feature'] == existing_feature['feature']:
                if feature['exten'] != existing_feature['exten'] or feature['enabled'] != existing_feature['enabled']:
                    return True
                else:
                    return False
