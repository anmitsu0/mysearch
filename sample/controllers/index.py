#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from sample.controllers import login, sign_up, refresh, search, manage, add_website, edit_profile


app = Bottle()


@app.get('/')
def index():
    file_name = __file__.split('/')[-1].split('.')[0]
    return {'message': 'This is sample_{} page.'.format(file_name)}


# resources/でアクセスできるRESTful API群を以下に羅列していく
app.mount('/login', login.app)
app.mount('/sign_up', sign_up.app)
app.mount('/refresh', refresh.app)
app.mount('/search', search.app)
app.mount('/admin', manage.app)
app.mount('/add_website', add_website.app)
app.mount('/edit_profile', edit_profile.app)
