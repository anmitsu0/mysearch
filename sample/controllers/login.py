#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, TEMPLATE_PATH
from sys import argv


app = Bottle()
TEMPLATE_PATH.append('./sample/view')


@app.route('/')
@app.jinja2_view('login.html')
def index():
    return {'message': 'This is sample_{} page.'.format(argv[0])}
