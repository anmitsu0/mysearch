#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import jinja2_template
from lib.bottle import request
from lib.bottle import redirect
from sample.models.data import user
from sample import config


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/', method=["GET", "POST"])
def index():
    login_page = "login.html"
    search_page = "search.html"
    manage_page = "manage.html"
    session = request.environ.get('beaker.session')
    # セッション情報が残っていた場合
    if session.get("user_id"):
        # 最後にどこかのページに訪問していた場合、そのページに移る
        if not session.get("last_stay_page"):
            session["last_stay_page"] = search_page
            session.save()
        redirect(redirect_url(session["last_stay_page"]))
    # 初回入場時
    if request.method == "GET":
        return jinja2_template(login_page)
    user_id = request.forms.get('user_id', "")
    user_password = request.forms.get('user_password', "")
    # ログイン認証
    if not user_id or not user_password:
        return jinja2_template(
            login_page,
            user_id=user_id,
            user_password=user_password,
            attention=u'ユーザーIDまたはパスワードの入力漏れがあります',
        )
    if not user.User().confirm_user(user_id, user_password):
        return jinja2_template(
            login_page,
            user_id=user_id,
            user_password=user_password,
            attention=u'ユーザーIDまたはパスワードに誤りがあります',
        )
    session["user_id"] = user_id
    # 管理ユーザーのid, passwordが入力されたとき
    if user_id == config.ADMIN_USER_INFO["id"] and user_password == config.ADMIN_USER_INFO["password"]:
        session["last_stay_page"] = manage_page
    # セッション切れのとき
    elif not session.get("last_stay_page"):
        session["last_stay_page"] = search_page
    session.save()
    return redirect(redirect_url(session["last_stay_page"]))


def redirect_url(page):
    return "/{0}/{1}".format(config.SECTION_NAME, page.replace(".html", ""))
