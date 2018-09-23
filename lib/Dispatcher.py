#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import importlib


class Dispatcher:
    DEFAULT_PROJECT_NAME = 'sample'
    DEFAULT_PAGE = 'index'
    DEFAULT_ACTION = 'index'
    DEFAULT_OPTION = ''
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
        self.current_option = self.DEFAULT_OPTION
        self.controller = None

    def dispatch(
            self,
            project_name=DEFAULT_PROJECT_NAME,
            page='',
            action='',
            option=''
    ):
        if project_name not in self.PAGE_LIST.keys():
            return

        # 1番目のパラメーターをコントローラー名(ページ名)として取得
        if page in self.PAGE_LIST[project_name]:
            self.current_page = page

        # (capitalize: 先頭の一文字を大文字、他を小文字にする)
        class_name = self.current_page.capitalize() + 'Controller'

        # クラスファイル読込
        module = importlib.import_module(project_name + '.controllers.' + class_name)

        # クラスインスタンス生成
        class_obj = getattr(module, class_name)
        self.controller = class_obj()

        # 2番目のパラメーターをメソッド名として取得
        if action:
            self.current_action = action

        # (lower: 全ての文字を小文字にする)
        action_name = self.current_action.lower() + '_action'

        # アクションメソッドを実行
        if hasattr(self.controller, action_name):
            action_method = getattr(self.controller, action_name)
            action_method()

        # 3番目のパラメーターをオプション情報として取得
        if option:
            self.current_option = option
