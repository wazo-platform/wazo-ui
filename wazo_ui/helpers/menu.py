# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session
from flask_menu.classy import classy_menu_item
from requests.exceptions import HTTPError

from .client import confd_client


def menu_filter(permission):
    def wrap():
        # TODO this check is done to handle case of the first user
        # An init should be done inside nconfd with the first user
        # to see identitiy menu and change what he can see.
        if 'visualization' not in session:
            return True

        if permission in session['visualization']:
            return True

        return False

    return wrap


def extract_permission(path):
    return path.lstrip('.')


def menu_item(path, text, **kwargs):
    permission = extract_permission(path)
    kwargs.setdefault('visible_when', menu_filter(permission))

    # Item without order use their label as order
    order = kwargs.setdefault('order', text)
    if isinstance(order, int):
        if order > 100:
            # Ugly hack to set order higher than items without order
            kwargs['order'] = 'zzz{}'.format(order)
        else:
            kwargs['order'] = '{0:03}'.format(order)

    return classy_menu_item(path, text, **kwargs)


def init_visualization():
    session.pop('visualization', None)

    visualization = _get_visualization(session['user']['uuid'])
    if visualization:
        session['visualization'] = visualization


def _get_visualization(user_uuid):
    try:
        return confd_client.users.get(user_uuid)['visualization']
    except HTTPError:
        return None
