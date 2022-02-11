# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import register_flaskview

from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .service import (
    GroupService,
    IdentityService,
    LDAPService,
    PolicyService,
    TenantService,
)
from .view import (
    GroupView,
    GroupListingView,
    IdentityView,
    IdentityListingView,
    LDAPConfigView,
    PolicyView,
    PolicyListingView,
    TenantView,
    TenantListingView,
)

identity = create_blueprint('identity', __name__)
identity_group = create_blueprint('identity_group', __name__)
tenant = create_blueprint('tenant', __name__)
ldap_config = create_blueprint('ldap', __name__)
policy = create_blueprint('policy', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        IdentityView.service = IdentityService(clients['wazo_auth'])
        IdentityView.register(identity, route_base='/identities')
        register_flaskview(identity, IdentityView)

        IdentityListingView.service = IdentityService(clients['wazo_auth'])
        IdentityListingView.register(identity, route_base='/identities_listing')

        register_listing_url('identity', 'identity.IdentityListingView:list_json')

        GroupView.service = GroupService(clients['wazo_auth'])
        GroupView.register(identity_group, route_base='/identity_groups')
        register_flaskview(identity_group, GroupView)

        GroupListingView.service = GroupService(clients['wazo_auth'])
        GroupListingView.register(identity_group, route_base='/identity_groups_listing')

        register_listing_url('identity_group', 'identity_group.GroupListingView:list_json')

        PolicyView.service = PolicyService(clients['wazo_auth'])
        PolicyView.register(policy, route_base='/policies')

        TenantView.service = TenantService(clients['wazo_auth'])
        TenantView.register(tenant, route_base='/tenants')
        register_flaskview(tenant, TenantView)

        TenantListingView.service = TenantService(clients['wazo_auth'])
        TenantListingView.register(tenant, route_base='/tenants_listing')

        register_listing_url('tenant', 'tenant.TenantListingView:list_json')

        register_flaskview(policy, PolicyView)

        PolicyListingView.service = PolicyService(clients['wazo_auth'])
        PolicyListingView.register(policy, route_base='/policies_listing')

        register_listing_url('policy', 'policy.PolicyListingView:list_json')

        LDAPConfigView.service = LDAPService(clients['wazo_auth'])
        LDAPConfigView.register(ldap_config, route_base='/ldap_config')
        register_flaskview(ldap_config, LDAPConfigView)

        core.register_blueprint(identity)
        core.register_blueprint(identity_group)
        core.register_blueprint(tenant)
        core.register_blueprint(ldap_config)
        core.register_blueprint(policy)
