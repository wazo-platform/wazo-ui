# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from flask import render_template
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Length

from wazo_ui.helpers.form import BaseForm
from wazo_ui.helpers.menu import menu_item, register_flaskview
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import BaseIPBXHelperView

asterisk_cli = create_blueprint('asterisk_cli', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        AsteriskCliView.service = AsteriskCliService(clients['wazo_amid'])
        AsteriskCliView.register(asterisk_cli, route_base='/asterisk_cli')
        register_flaskview(asterisk_cli, AsteriskCliView)

        core.register_blueprint(asterisk_cli)


class AsteriskCliForm(BaseForm):
    command = StringField('Command', [InputRequired, Length(max=128)])
    submit = SubmitField('Submit')


class AsteriskCliView(BaseIPBXHelperView):
    form = AsteriskCliForm
    resource = 'asterisk_cli'

    @menu_item('.ipbx.global_settings.asterisk_cli', 'Asterisk CLI', icon="terminal")
    def index(self):
        return render_template(
            self._get_template('list'), form=self._populate_form(self.form())
        )

    def post(self):
        resources = self._map_form_to_resources_post(self.form())
        data = self.service.send_cmd(resources.get('command'))
        return render_template(
            self._get_template('list'),
            form=self._populate_form(self.form()),
            results=data,
        )


class AsteriskCliService:
    def __init__(self, amid_client):
        self._amid = amid_client

    def send_cmd(self, cmd):
        return self._amid.command(cmd)['response']
