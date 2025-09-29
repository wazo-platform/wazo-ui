# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session, url_for
from flask_login.mixins import UserMixin


class UserUI(UserMixin):
    def __init__(self, token, uuid=None):
        self.token = token
        self.uuid = uuid
        if 'config' not in session:
            session['config'] = {}
        if 'tenants' not in session:
            session['tenants'] = []

    def get_id(self):
        return self.token

    def get_user(self):
        return session.get('user')

    def get_user_tenant_uuid(self):
        return session['user'].get('tenant_uuid')

    def get_displayname(self):
        return session['user']['username']

    def get_tenant_uuid(self):
        if 'working_tenant_uuid' in session:
            return session['working_tenant_uuid']

        return session['user'].get('tenant_uuid')

    def get_user_index_url(self):
        return url_for('user.UserView:index')

    def get_current_tenants(self):
        return session['tenants'] if 'tenants' in session else []

    def reset(self):
        session['config'] = {}
        session['tenants'] = []

    def get_config(self):
        return session['config']

    def set_config(self, config):
        session['config'] = {'websocketd': config['websocketd']}

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
