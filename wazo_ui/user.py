# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session, url_for
from flask_login.mixins import UserMixin


class UserUI(UserMixin):

    def __init__(self, token, uuid=None):
        self.token = token
        self.uuid = uuid
        if 'instance' not in session:
            session['instance'] = None

    def get_id(self):
        return self.token

    def get_user(self):
        return session.get('user')

    def get_tenant(self):
        return session.get('user_tenant')

    def get_displayname(self):
        return session['user']['username']

    def get_tenant_uuid(self):
        if 'working_tenant_uuid' in session:
            return session['working_tenant_uuid']

        return session['user'].get('tenant_uuid')

    def get_user_index_url(self):
        return url_for('wazo_engine.user.UserView:index')

    def get_current_tenants(self):
        instance = self.get_instance()
        if not instance:
            return []

        return session['tenants'] if 'tenants' in session else []

    def reset_instance(self):
        session['instance'] = None
        session['tenants'] = []

    def set_tenant(self, tenant=None):
        session['instance'] = {}
        session['instance']['wazo_tenant'] = tenant

    def set_instance_config(self, config):
        if not session['instance']:
            session['instance'] = {}

        session['instance']['config'] = {'websocketd': config['websocketd']}

    def get_instance(self):
        return session['instance']

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
