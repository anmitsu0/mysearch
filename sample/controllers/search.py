#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import jinja2_template
from lib.bottle import request


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/')
def index():
    search_page = "search.html"
    login_page = "login.html"
    session = request.environ.get('beaker.session')
    # セッション情報が残っていた場合
    if session.get("user_id"):
        return jinja2_template(search_page)
    else:
        # session["last_stay_page"] = search_page
        return jinja2_template(login_page)
