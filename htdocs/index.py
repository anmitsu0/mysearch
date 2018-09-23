#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import route, run, static_file, error
from lib.Dispatcher import Dispatcher


@route('/', name='index')
@route('/<page>', name='index')
@route('/<page>/<action>', name='index')
@route('/<page>/<action>/<option:path>', name='index')
def index(page='', action='', option=''):
    dispatcher = Dispatcher()
    dispatcher.dispatch(page=page, action=action, option=option)


@route('/static/<file_path:path>', name="static_file")
def static(file_path):
    return static_file(file_path, root="./static")


@error(404)
def error404(error):
    return '''
        <img src="/static/error.jpg">
        {error}
    '''.format(error=error)


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
