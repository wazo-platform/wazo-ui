# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import AccessFeaturesService
from .view import AccessFeatureView, AccessFeaturesListingView

access_features = create_blueprint('access_features', __name__)


class Plugin(object):
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']
        service = AccessFeaturesService(clients['wazo_confd'])

        AccessFeatureView.service = service
        AccessFeatureView.register(access_features, route_base='/access_features')
        register_flaskview(access_features, AccessFeatureView)

        AccessFeaturesListingView.service = service
        AccessFeaturesListingView.register(
            access_features, route_base='/access_features_listing'
        )

        register_listing_url(
            'access_features_by_type',
            'access_features.AccessFeaturesListingView:list_json_by_type',
        )
        register_listing_url(
            'access_features', 'access_features.AccessFeaturesListingView:list_json'
        )
        register_listing_url(
            'access_features_with_id',
            'access_features.AccessFeaturesListingView:list_json_with_id',
        )

        core.register_blueprint(access_features)
