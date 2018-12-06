#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import jinja2_template
from lib.bottle import request
from sample.models.data import user


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/', method=["GET", "POST"])
def index():
    sign_up_page = "sign_up.html"
    login_page = "login.html"
    search_page = "search.html"
    session = request.environ.get('beaker.session')
    # セッション情報が残っていた場合
    if session.get("user_id"):
        # 最後にどこかのページに訪問していた場合、そのページに移る
        if session.get("last_stay_page"):
            return jinja2_template(session["last_stay_page"])
        else:
            return jinja2_template(search_page)
    # 初回入場時
    if request.method == "GET":
        return jinja2_template(sign_up_page)
    user_id = request.forms.get('user_id', "")
    user_password = request.forms.get('user_password', "")
    # ユーザー登録
    if not user_id or not user_password:
        return jinja2_template(
            sign_up_page,
            user_id=user_id,
            user_password=user_password,
            attention=u'ユーザーIDまたはパスワードの入力漏れがあります',
        )
    if user.User().confirm_user_id(user_id):
        return jinja2_template(
            sign_up_page,
            user_id=user_id,
            user_password=user_password,
            attention=u'既に登録済みのユーザーIDです',
        )
    user.User().register_user(user_id, user_password)
    return jinja2_template(
        login_page,
        user_id=user_id,
        user_password=user_password
    )
