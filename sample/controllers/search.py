#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.bottle import Bottle
from lib.bottle import TEMPLATE_PATH
from lib.bottle import jinja2_template
from lib.bottle import request
from sample.models.data import website


app = Bottle()
TEMPLATE_PATH.append('../sample/views')


@app.route('/', method=["GET", "POST"])
def index():
    search_page = "search.html"
    login_page = "login.html"
    session = request.environ.get('beaker.session')
    user_id = session.get("user_id", "")
    # セッション情報が残っていた場合
    if user_id:
        cls_website = website.Website()
        search_word = request.forms.decode().get('search_word', "")
        delete_website_ids = request.forms.getall('delete_website_ids')
        complete_delete_websites = "False"
        if delete_website_ids:
            # print("\tdelete_website_ids: {}".format(delete_website_ids))
            cls_website.delete_websites(user_id, delete_website_ids)
            complete_delete_websites = "True"
        websites = cls_website.get_websites(user_id)
        search_word_hit_count = list()
        if search_word:
            search_word_hit_count = cls_website.search_word_hit_count(user_id, search_word)
            # 検索ヒット数が0のものを除く
            num0_indeces = [i for i, x in enumerate(search_word_hit_count) if x != 0]
            websites = [websites[i] for i in num0_indeces]
            search_word_hit_count = [search_word_hit_count[i] for i in num0_indeces]
            # 検索ヒット数の多い順に並び替える
            if len(num0_indeces) > 1:
                websites, search_word_hit_count = zip(*sorted(
                    zip(websites, search_word_hit_count),
                    key=lambda x: x[1],
                    reverse=True
                ))
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
