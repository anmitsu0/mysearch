#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, TEMPLATE_PATH, jinja2_template
from sample.controllers import refresh


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/')
def index():
    file_name = __file__.split('/')[-1].split('.')[0]
    refresh.footprint(file_name)
    return jinja2_template('add_website.html')
