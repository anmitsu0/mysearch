#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from lib.bottle import Bottle, TEMPLATE_PATH, jinja2_template, request
# from sample.models.data import user


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/')
def index():
    return jinja2_template('login.html')


@app.route('/', method='POST')
def index():
    user_name = request.forms.get('user_name')
    user_name = '' if user_name is None else str(user_name)
    user_password = request.forms.get('user_password')
    user_password = '' if user_password is None else str(user_password)
    if len(user_name) != 0 or len(user_password) != 0:
        return jinja2_template(
            'login.html',
            attention=u'ユーザー名またはパスワードの入力漏れがあります',
        )
    # if not user.is_correct(user_name=user_name, user_password=user_password):
    #     return jinja2_template(
    #         'login.html',
    #         attention=u'ユーザー名またはパスワードが間違っています',
    #     )
    # if not is_correct_url(url=request.url):
    #     return jinja2_template(
    #         'login.html',
    #         attention=u'不正なアクセスです',
    #     )
    # user_secret_id = user.get_secret_id(
    #     user_name=user_name, user_password=user_password
    # )
    # return jinja2_template('refresh.html', user_secret_id=user_secret_id)
    return jinja2_template(
        'refresh.html',
        user_name=user_name,
        user_password=user_password
    )
