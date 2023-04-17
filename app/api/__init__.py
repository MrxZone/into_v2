#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import pkgutil


def init_routers(app):
    '''
    初始化 router
    '''

    def split_path(modules):
        router_modules = []
        for o in modules:
            router_modules.append("api{}".format(o.split("api")[1]))
        return router_modules

    def find_modules(paths):
        '''
        查找路径下的所有 module
        '''
        modules = []
        for finder, name, ispkg in pkgutil.iter_modules(paths):
            if ispkg:
                modules.extend(find_modules(['{}/{}'.format(finder.path, name)]))
            else:
                module_path = '{}/{}'.format(finder.path, name)
                modules.append(module_path.replace('/', '.'))

        return modules

    router_modules = find_modules(['app/api'])
    router_modules = split_path(router_modules)
    for name in router_modules:
        module = importlib.import_module(name)
        prefix = ("." + name).replace('.', '/')
        if not hasattr(module, 'router'):
            continue
        _router = getattr(module, 'router')
        app.include_router(_router, prefix=prefix)
