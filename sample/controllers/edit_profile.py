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
    edit_profile_page = "edit_profile.html"
    login_page = "login.html"
    session = request.environ.get('beaker.session')
    user_id = session.get("user_id", "")
    # セッション情報が残っていた場合
    if user_id:
        cls_user = user.User()
        attention = u''
        current_password = request.forms.get('current_password', "")
        new_password = request.forms.get('new_password', "")
        re_new_password = request.forms.get('re_new_password', "")
        complete_update_password = request.forms.get('complete_update_password', "False")
        if request.method == "POST":
            if not current_password or not new_password or not re_new_password:
                attention = u'入力漏れがあります'
                complete_update_password = "False"
            if new_password != re_new_password:
                attention = u'新しいパスワード(確認用)に同じものを入力してください'
                complete_update_password = "False"
            if not cls_user.confirm_user(user_id, current_password):
                attention = u'現在のパスワードが登録情報と異なります'
                complete_update_password = "False"
        if complete_update_password == "True":
            cls_user.update_password(user_id, current_password, new_password)
        return jinja2_template(
            edit_profile_page,
            attention=attention,
            user_id=user_id,
            current_password=current_password,
            new_password=new_password,
            re_new_password=re_new_password,
            complete_update_password=complete_update_password
        )
    else:
        session["last_stay_page"] = edit_profile_page
        return jinja2_template(login_page)
