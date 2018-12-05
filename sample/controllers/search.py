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
        cls_website = website.Website()
        search_word = request.forms.get('search_word', "")
        search_word_hit_count = request.forms.get('search_word_hit_count', None)
        delete_website_ids = request.forms.get('delete_website_ids', [])
        complete_delete_websites = "False"
        if delete_website_ids:
            cls_website.delete_websites(user_id, delete_website_ids)
            complete_delete_websites = "True"
        websites = None
        if search_word:
            websites = cls_website.get_websites_with_search_word(user_id, search_word)
            if not search_word_hit_count:
                search_word_hit_count = cls_website.search_word_hit_count(user_id, search_word)
        else:
            websites = request.forms.get('websites', None)
            websites = websites if websites else cls_website.get_websites(user_id)
        return jinja2_template(
            search_page,
            user_id=user_id,
            websites=websites,
            search_word=search_word,
            search_word_hit_count=search_word_hit_count,
            complete_delete_websites=complete_delete_websites
        )
    else:
        session["last_stay_page"] = search_page
        return jinja2_template(login_page)
