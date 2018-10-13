#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, TEMPLATE_PATH, jinja2_view
from sys import argv


app = Bottle()
TEMPLATE_PATH.append('./sample/views')


@app.route('/')
@jinja2_view('login.html')
def index():
    return {
        'message': 'This is sample_{} page.'.format(argv[0]),
        'title': u'ログイン'
    }
