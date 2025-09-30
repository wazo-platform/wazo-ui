# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..http_server import app


def menu_item(path, text, **kwargs):
    kwargs['visible_when'] = lambda: True

    # Item without order use their label as order
    order = kwargs.setdefault('order', text)
    if isinstance(order, int):
        # Ugly hack to set order higher than items without order
        if order > 100 and order < 1000:
            kwargs['order'] = f'yyy{order}'
        elif order > 999:
            kwargs['order'] = f'zzz{order}'
        else:
            kwargs['order'] = f'{order:03}'

    def func_wrap(func):
        item = dict(path=path, text=text, **kwargs)

        if hasattr(func, "_menu_items"):
            func._menu_items.append(item)
        else:
            func._menu_items = [item]

        return func

    return func_wrap


def register_flaskview(blueprint, classful_view):
    for method_str in dir(classful_view):
        method = getattr(classful_view, method_str)
        if hasattr(method, "_menu_items"):
            for menu_item in method._menu_items:
                endpoint = (
                    f'{blueprint.name}.{classful_view.__name__}:{method.__name__}'
                )
                path = menu_item.pop('path')
                item = app.extensions['menu'].root_node.submenu(path)
                item.register(endpoint, **menu_item)
