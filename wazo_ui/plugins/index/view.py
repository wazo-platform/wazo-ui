# Copyright 2018 The Wazo Authors (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import url_for, redirect, render_template, request, session
from flask_login import current_user

from wazo_ui.helpers.classful import BaseHelperView, LoginRequiredView


class IndexView(BaseHelperView):

    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login.Login:get'))

        return render_template('index.html')


class WorkingTenantView(LoginRequiredView):
    def set_working_instance_tenant(self):
        session['working_instance_tenant_uuid'] = request.args.get('tenant_uuid')
        return redirect(request.referrer)
