#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, request, redirect
from beaker.middleware import SessionMiddleware


# セッションの設定
session_opts = {
    'session.type': 'file',
    'session.data_dir': '../data/logs',
    'session.cookie_expires': True,
    'session.auto': True,
}


app = Bottle()
apps = SessionMiddleware(app, session_opts)


def make_secret_id(user_name, user_password):
    """
    ユーザー名とパスワードから、難読化したsecret_idを生成

    :param user_name:
    :param user_password:
    :return: secret_id (str)
    """
    return user_name + user_password  # 後で修正


def update_secret_id(secret_id):
    """
    セッション内のuser_secret_idを更新

    :param secret_id:
    :return: (void)
    """
    session = request.environ.get('beaker.session')
    if secret_id is not None:
        session['secret_id'] = str(secret_id)


def last_visit_website_name():
    """
    最後に訪れたサイト名

    :return: file_name (str)
    """
    session = request.environ.get('beaker.session')
    if 'file_name' not in session:
        session['file_name'] = 'search'
    return session['file_name']


def footprint(file_name):
    """
    最後に訪れたサイト名を更新
    セッションが切れていた場合、ログイン画面に戻る

    :return: (void)
    """
    session = request.environ.get('beaker.session')
    if file_name is None or file_name == '':
        # user_nameがadminなら'manage'にする
        session['file_name'] = 'search'
    else:
        session['file_name'] = str(file_name)
    if 'secret_id' not in session:
        redirect('login.html')
