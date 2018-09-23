#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import route, run, view, static_file, url
from lib.bottle import request
from lib.bottle import error


@route('/static/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root="./static")

@route('/', name="index")
@view("index_template")
def index():
    return dict(url=url)


@route('/<name>/<count:int>', name="hello")
@view("hello_template")
def hello(name, count):
    return dict(name=name, count=count, url=url)



@route('/login', method='GET') # or @get('/login')
def login():
    username = request.query.get('user')
    password = request.query.get('pass')

    #GETで何も渡されていない時はusername,passwordに何も入れない
    username = "" if username is None else username
    password = "" if password is None else password

    return '''
	<form action="/login" method="post">
		Username: <input name="username" type="text" value="{username}"/>
		Password: <input name="password" type="password" value="{password}"/>
		<input value="Login" type="submit" />
	</form>
	'''.format(username=username, password=password)


@route('/login', method='POST') # or @post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    return "{username} {password}".format(username=username, password=password)


@error(404)
def error404(error):
    return '''
		<img src="/static/error.jpg">
		{error}
	'''.format(error=error)



if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)

