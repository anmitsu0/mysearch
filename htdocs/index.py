#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import route, run
from lib.Dispatcher import Dispatcher


@route('/', name='index')
@route('/<page>', name='index')
@route('/<page>/<action>', name='index')
@route('/<page>/<action>/<option:path>', name='index')
def index(page='', action='', option=''):
    dispatcher = Dispatcher()
    dispatcher.dispatch(page=page, action=action, option=option)


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
