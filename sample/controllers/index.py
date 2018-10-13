#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from sys import argv
from sample.controllers import login, search, manage, add_website, edit_profile


app = Bottle()


@app.get('/')
def index():
    return {'message': 'This is sample_{} page.'.format(argv[0])}


# resources/でアクセスできるRESTful API群を以下に羅列していく
app.mount('/login', login.app)
app.mount('/search', search.app)
app.mount('/admin', manage.app)
app.mount('add_website', add_website.app)
app.mount('/edit_profile', edit_profile.app)
