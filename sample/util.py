#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import request
from sample import config


def redirect_url(page):
    return "/{0}/{1}".format(config.SECTION_NAME, page.replace(".html", ""))


def reset_session():
    session = request.environ.get('beaker.session')
    if session.get("user_id"):
        session["user_id"] = ""
    if session.get("last_stay_page"):
        session["last_stay_page"] = ""
