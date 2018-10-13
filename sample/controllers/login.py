#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle, request
from sys import argv


app = Bottle()


@app.route('/login', method='POST')
def index():
    user_id = request.forms.get('user_id')
    user_name = request.forms.get('user_name')
    user_password = request.forms.get('user_password')
    return {
        'message': 'This is sample_{} page.'.format(argv[0]),
        'user_id': user_id if user_id is not None else '',
        'user_name': user_name if user_name is not None else '',
        'user_password': user_password if user_password is not None else '',
    }
