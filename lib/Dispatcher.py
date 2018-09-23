#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import importlib


class Dispatcher:
    DEFAULT_PROJECT_NAME = 'sample'
    DEFAULT_PAGE = 'index'
    DEFAULT_ACTION = 'index'
    PAGE_LIST = {
        DEFAULT_PROJECT_NAME: [
            DEFAULT_PAGE,
            'login',
            'search',
            'admin',
            'add_website',
            'edit_profile',
        ],
    }

    def __init__(self):
        self.current_page = self.DEFAULT_PAGE
        self.current_action = self.DEFAULT_ACTION
        self.controller = None

    def dispatch(self, project_name=DEFAULT_PROJECT_NAME, request_uri=''):
        if project_name not in self.PAGE_LIST.keys() or not request_uri:
            return

        params = request_uri.split('/')
        # 1番目のパラメーターをコントローラー名(ページ名)として取得
        if len(params) > 0 and params[0] in self.PAGE_LIST[project_name]:
            self.current_page = params[0]

        # (capitalize: 先頭の一文字を大文字、他を小文字にする)
        class_name = self.current_page.capitalize() + 'Controller'

        # クラスファイル読込
        module = importlib.import_module(project_name + '.controllers.' + class_name)

        # クラスインスタンス生成
        class_obj = getattr(module, class_name)
        self.controller = class_obj()

        # 2番目のパラメーターをメソッド名として取得
        if len(params) > 1:
            self.current_action = params[1]

        # (lower: 全ての文字を小文字にする)
        action_name = self.current_action.lower() + '_action'

        # アクションメソッドを実行
        if hasattr(self.controller, action_name):
            action_method = getattr(self.controller, action_name)
            action_method()
