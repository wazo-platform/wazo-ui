# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import Blueprint


def create_blueprint_core(name, import_name, url_prefix=None):
    return Blueprint(
        name,
        import_name,
        template_folder='templates',
        static_folder='static',
        static_url_path='/%s' % import_name,
        url_prefix=url_prefix,
    )


def create_blueprint(name, import_name):
    return Blueprint(
        'wazo_engine.{}'.format(name),
        import_name,
        template_folder='templates',
        static_folder='static/wazo_engine',
        static_url_path='/%s' % import_name,
        url_prefix='/engine',
    )
