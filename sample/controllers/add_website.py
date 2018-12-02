#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import jinja2_template


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/')
def index():
    file_name = __file__.split('/')[-1].split('.')[0]
    return jinja2_template('add_website.html')
