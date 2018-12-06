#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from sample.controllers import login
from sample.controllers import sign_up
from sample.controllers import search
from sample.controllers import manage
from sample.controllers import add_website
from sample.controllers import edit_profile
from sample.controllers import logout


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


# resources/でアクセスできるRESTful API群を以下に羅列していく
app.mount('/login', login.app)
app.mount('/sign_up', sign_up.app)
app.mount('/search', search.app)
app.mount('/manage', manage.app)
app.mount('/add_website', add_website.app)
app.mount('/edit_profile', edit_profile.app)
app.mount("/logout", logout.app)


@app.get('/')
def index():
    return str('Hello. This is sample_top page.')
