#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import static_file, error


def static(file_path):
    return static_file(file_path, root="./static")


@error(404)
def error404(error):
    return '''
        <img src="/static/error.jpg">
        {error}
    '''.format(error=error)
