#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from lib.bottle import Bottle, run
from beaker.middleware import SessionMiddleware
from sample.controllers import index as sample_index


# セッションの設定
session_opts = {
    'session.type': 'file',
    'session.data_dir': '/tmp',
    'session.cookie_expires': True,
    'session.auto': True,
}


app = Bottle()
apps = SessionMiddleware(app, session_opts)


@app.route('/')
def index():
    return str('Hello. This is top page.')


if __name__ == '__main__':
    # 以下のindex.py(sample/controllers/index.py)で、さらに別のroutesを指定することも可能。
    # このようにワンクッション置くことで、/sampleと言うようなURLのみの場合にも何かメッセージを表示することが可能。
    app.mount('/sample', sample_index.app)

    run(app=apps, host='localhost', port=8080, debug=True, reloader=True)
