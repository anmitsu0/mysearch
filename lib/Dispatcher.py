#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import importlib


class Dispatcher:
    DEFAULT_ROOT_PAGE = 'index'
    DEFAULT_PROJECT_NAME = 'sample'
    PAGE_LIST = {
        DEFAULT_PROJECT_NAME: [
            DEFAULT_ROOT_PAGE,
            'login',
            'search',
            'admin',
            'add_website',
            'edit_profile',
        ],
    }

    def __init__(self, root_page=DEFAULT_ROOT_PAGE):
        self.root_page = root_page
        self.controller = None

    def dispatch(self, project_name=DEFAULT_PROJECT_NAME, request_uri=''):
        if project_name not in self.PAGE_LIST.keys() or not request_uri:
            return

        params = request_uri.split('/')
        # 1番目のパラメーターを取得
        if len(params) > 0 and params[0] in self.PAGE_LIST[project_name]:
            self.root_page = params[0]

        # capitalize:先頭の一文字を大文字、他を小文字にする
        class_name = self.root_page.capitalize() + 'Controller'
        module = importlib.import_module(project_name + '.controllers.' + class_name)
        class_obj = getattr(module, class_name)
        self.controller = class_obj()
