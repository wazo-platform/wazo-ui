# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_menu.classy import classy_menu_item


def menu_item_aux(path, text, **kwargs):
    kwargs['visible_when'] = lambda: True

    # Item without order use their label as order
    order = kwargs.setdefault('order', text)
    if isinstance(order, int):
        if order > 100:
            # Ugly hack to set order higher than items without order
            kwargs['order'] = 'zzz{}'.format(order)
        else:
            kwargs['order'] = '{0:03}'.format(order)

    return classy_menu_item(path, text, **kwargs)


def menu_item(path, *args, **kwargs):
    return menu_item_aux(path, *args, **kwargs)
