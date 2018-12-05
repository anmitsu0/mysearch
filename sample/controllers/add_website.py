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
    add_website_page = "add_website.html"
    login_page = "login.html"
    session = request.environ.get('beaker.session')
    user_id = session.get("user_id", "")
    # セッション情報が残っていた場合
    if user_id:
        cls_website = website.Website()
        website_name = request.forms.decode().get('website_name', "")
        website_link = request.forms.decode().get('website_link', "")
        website_keywords = request.forms.decode().get('website_keywords', "")
        complete_add_website = request.forms.get('complete_add_website', "False")
        if website_link:
            if not website_name:
                # エラー(URL入力済かつ、サイト名が何も書かれていない状態で、サイト登録ボタンを押した場合)
                if website_keywords:
                    return jinja2_template(
                        add_website_page,
                        attention=u'サイト名を入力してください',
                        website_link=website_link,
                        website_keywords=website_keywords,
                        complete_add_website="False"
                    )
                website_name = cls_website.get_website_title_with_link(website_link)
            website_keywords = cls_website.get_website_keywords_with_link(website_link)
            if complete_add_website == "True":
                cls_website.add_website(user_id, website_name, website_link, website_keywords)
        elif complete_add_website == "True":
            # エラー(URL入力まだの状態で、サイト登録ボタンを押した場合)
            return jinja2_template(
                add_website_page,
                attention=u'URL入力を先に行ってください',
                complete_add_website="False"
            )
        return jinja2_template(
            add_website_page,
            user_id=user_id,
            website_name=website_name,
            website_link=website_link,
            website_keywords=website_keywords,
            complete_add_website=complete_add_website
        )
    else:
        session["last_stay_page"] = add_website_page
        return jinja2_template(login_page)
