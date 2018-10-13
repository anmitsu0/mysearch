#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, TEMPLATE_PATH, jinja2_view
from sys import argv


app = Bottle()
TEMPLATE_PATH.append('./sample/views')


@app.get('/')
@jinja2_view('search.html')
def index():
    return {
        'message': 'This is sample_{} page.'.format(argv[0]),
    }