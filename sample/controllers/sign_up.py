#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, TEMPLATE_PATH, jinja2_template, request


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/', name='init')
def index():
    return jinja2_template('sign_up.html')


@app.route('/', method='POST', name='confirm')
def index():
    user_name = request.forms.get('user_name')
    user_name = '' if user_name is None else str(user_name)
    user_password = request.forms.get('user_password')
    user_password = '' if user_password is None else str(user_password)
    if len(user_name) == 0 or len(user_password) == 0:
        return jinja2_template(
            'sign_up.html',
            attention=u'ユーザー名またはパスワードの入力漏れがあります',
        )
    # if user.find_password(user_password=user_password):
    #     return jinja2_template(
    #         'sign_up.html',
    #         attention=u'使用済みのパスワードです',
    #     )
    # user.make_id(
    #     user_name=user_name, user_password=user_password
    # )
    return jinja2_template('login.html')
