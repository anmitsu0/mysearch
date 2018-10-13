#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, TEMPLATE_PATH, jinja2_view


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.get('/')
@jinja2_view('refresh.html')
def index():
    file_name = __file__.split('/')[-1].split('.')[0]
    return {'message': 'This is sample_{} page.'.format(file_name)}
