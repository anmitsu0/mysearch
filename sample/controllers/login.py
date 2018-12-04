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
        return jinja2_template(login_page)
    user_id = request.forms.get('user_id', "")
    user_password = request.forms.get('user_password', "")
    # ログイン認証
    if not user_id or not user_password:
        return jinja2_template(
            login_page,
            attention=u'ユーザー名またはパスワードの入力漏れがあります',
        )
    if not user.User().confirm_user(user_id, user_password):
        return jinja2_template(
            login_page,
            attention=u'既に登録済みのユーザー名とパスワードです',
        )
    session["user_id"] = user_id
    session["last_stay_page"] = search_page
    session.save()
    return jinja2_template(search_page)

