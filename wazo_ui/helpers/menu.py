# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_login import current_user
from flask_menu.classy import classy_menu_item


def menu_item_aux(path, text, **kwargs):
    kwargs.setdefault('visible_when', True)

    # Item without order use their label as order
    order = kwargs.setdefault('order', text)
    if isinstance(order, int):
        if order > 100:
            # Ugly hack to set order higher than items without order
            kwargs['order'] = 'zzz{}'.format(order)
        else:
            kwargs['order'] = '{0:03}'.format(order)

    return classy_menu_item(path, text, **kwargs)


def _is_root_and_has_permission():
    def wrap():
        if current_user.get_instance().get('wazo_tenant'):
            return False
        return True
    return wrap


def menu_item(path, *args, **kwargs):
    multi_tenant = kwargs.get('multi_tenant', False)
    if not multi_tenant:
        kwargs['visible_when'] = _is_root_and_has_permission()

    return menu_item_aux(path, *args, **kwargs)
