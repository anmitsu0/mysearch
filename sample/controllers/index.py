#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, TEMPLATE_PATH, jinja2_template
from sample.controllers import login, sign_up, search, manage, add_website, edit_profile


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


# resources/でアクセスできるRESTful API群を以下に羅列していく
app.mount('/login', login.app)
app.mount('/sign_up', sign_up.app)
app.mount('/search', search.app)
app.mount('/admin', manage.app)
app.mount('/add_website', add_website.app)
app.mount('/edit_profile', edit_profile.app)


@app.get('/')
def index():
    return str('Hello. This is sample_top page.')
