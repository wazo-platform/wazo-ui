# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import Blueprint


def create_blueprint(name, import_name):
    return Blueprint(
        name,
        import_name,
        template_folder='templates',
        static_folder='static',
        static_url_path=f'/{import_name}',
    )
