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


@app.route('/')
def index():
    manage_page = "manage.html"
    login_page = "login.html"
    session = request.environ.get('beaker.session')
    user_id = session.get("user_id", "")
    # セッション情報が残っていた場合
    if user_id:
        cls_user = db_user.User()
        cls_website = db_website.Website()
        users_data = cls_user.get_users()
        users = list(dict())
        for i in users_data.count():
            users[i]["index"] = i
            user_id = users_data[i].get("id", "")
            users[i]["id"] = user_id if user_id else ""
            users[i]["websites"] = cls_website.get_websites(users[i]["id"]) if user_id else []
        delete_user_ids = request.forms.get('delete_user_ids', [])
        complete_delete_user = "False"
        if delete_user_ids:
            cls_user.delete_users(delete_user_ids)
            complete_delete_user = "True"
        return jinja2_template(
            manage_page,
            users=users,
            complete_delete_user=complete_delete_user
        )
    else:
        session["last_stay_page"] = manage_page
        return jinja2_template(login_page)
