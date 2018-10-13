#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, request
from sys import argv


app = Bottle()


@app.route('/')
def index():
    return {'message': 'This is sample_{} page.'.format(argv[0])}
