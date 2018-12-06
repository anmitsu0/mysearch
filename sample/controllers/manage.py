#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import jinja2_template
from lib.bottle import request
from sample.models.data import user as db_user
from sample.models.data import website as db_website


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/', method=["GET", "POST"])
def index():
    manage_page = "manage.html"
    login_page = "login.html"
    session = request.environ.get('beaker.session')
    user_id = session.get("user_id", "")
    # セッション情報が残っていた場合
    if user_id:
        cls_user = db_user.User()
        cls_website = db_website.Website()
        delete_user_ids = request.forms.getall('delete_user_ids')
        # (管理ユーザーのuser_idは除く)
        if user_id in delete_user_ids:
            delete_user_ids.remove(user_id)
        complete_delete_user_and_websites = "False"
        if delete_user_ids:
            # print(user_id, delete_user_ids)
            cls_user.delete_users(delete_user_ids)
            cls_website.delete_websites_with_user_ids(delete_user_ids)
            complete_delete_user_and_websites = "True"
        users_data = cls_user.get_users()
        users = list()
        for i in range(len(users_data)):
            user = dict()
            user["id"] = tmp_user_id = users_data[i].get("id", "")
            user["_id"] = users_data[i].get("_id", "")
            user["websites"] = cls_website.get_websites(user["id"]) if tmp_user_id else []
            users.append(user)
        return jinja2_template(
            manage_page,
            users=users,
            complete_delete_user_and_websites=complete_delete_user_and_websites
        )
    else:
        session["last_stay_page"] = manage_page
        return jinja2_template(login_page)
