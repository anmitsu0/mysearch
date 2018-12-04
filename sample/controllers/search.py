#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import jinja2_template
from lib.bottle import request
from sample.models.data import website


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/')
def index():
    search_page = "search.html"
    login_page = "login.html"
    session = request.environ.get('beaker.session')
    user_id = session.get("user_id", "")
    # セッション情報が残っていた場合
    if user_id:
        delete_website_ids = request.forms.get('delete_website_ids', "")
        website.Website().delete_website(user_id, delete_website_ids)
        search_word = request.forms.get('search_word', "")
        websites = None
        if search_word:
            websites = website.Website().get_websites_with_search_word(user_id, search_word)
        else:
            websites = request.forms.get('websites', None)
            websites = websites if websites else website.Website().get_websites(user_id)
        search_word_relevance = request.forms.get('search_word_relevance', "")
        search_word_hit_count = request.forms.get('search_word_hit_count', "")
        return jinja2_template(
            search_page,
            websites=websites,
            search_word=search_word,
            search_word_relevance=search_word_relevance,
            search_word_hit_count=search_word_hit_count,
        )
    else:
        # session["last_stay_page"] = search_page
        return jinja2_template(login_page)
