#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import redirect
from sample import util


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/')
def index():
    login_page = "login.html"
    util.reset_session()
    return redirect(util.redirect_url(login_page))
