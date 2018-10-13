#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from lib.bottle import Bottle
from sample.controllers import index as sample_index


root = Bottle()


@root.route('/')
def index():
    return str('Hello. This is top page.')


if __name__ == '__main__':
    # 以下のindex.py(sample/controllers/index.py)で、さらに別のroutesを指定することも可能。
    # このようにワンクッション置くことで、/sampleと言うようなURLのみの場合にも何かメッセージを表示することが可能。
    root.mount('/sample', sample_index.app)

    root.run(host='localhost', port=8080, debug=True, reloader=True)
