#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import jinja2_template
from lib.bottle import request
from sample.models.data import user


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/')
def index():
    edit_profile_page = "edit_profile.html"
    login_page = "login.html"
    session = request.environ.get('beaker.session')
    user_id = session.get("user_id", "")
    # セッション情報が残っていた場合
    if user_id:
        cls_user = user.User()
        user_id = request.forms.get('user_id', "")
        user_password = request.forms.get('user_password', "")
        confirm_user = request.forms.get('confirm_user', "False")
        complete_update_user = request.forms.get('complete_update_user', "False")
        if confirm_user == "True" and not cls_user.confirm_user(user_id, user_password):
            # エラー(現在の～：該当なし）
            return jinja2_template(
                edit_profile_page,
                attention=u'ユーザー名またはパスワードが登録情報と異なります',
                user_id=user_id,
                user_password=user_password,
                confirm_user="False"
            )
        if complete_update_user == "True" and cls_user.confirm_user(user_id, user_password):
            # エラー(新しい～：重複あり)
            return jinja2_template(
                edit_profile_page,
                attention=u'別のユーザー名・パスワードを使用してください',
                user_id=user_id,
                user_password=user_password,
                confirm_user=confirm_user,
                complete_update_user="False"
            )
        return jinja2_template(
            edit_profile_page,
            user_id=user_id,
            user_password=user_password,
            confirm_user=confirm_user,
            complete_update_user=complete_update_user
        )
    else:
        session["last_stay_page"] = edit_profile_page
        return jinja2_template(login_page)
