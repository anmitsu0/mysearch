#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
import requests
from bs4 import BeautifulSoup
from lib.bottle import Bottle
from sample.models.data import db
from sample import config


app = Bottle()


class Website(db.DB):
    _TABLE_NAME = "website"

    def __init__(self):
        super(Website, self).__init__()
        if not self.is_exist_table(self._TABLE_NAME):
            self.create_table()

    def create_table(self):
        try:
            self.curs.execute("""
                CREATE TABLE {}(
                _id int NOT NULL AUTO_INCREMENT,
                user_id int(20) NOT NULL,
                name varchar NOT NULL,
                link varchar NOT NULL,
                keywords varchar NOT NULL,
                most_frequent_word varchar,
                create_date datetime NOT NULL,
                PRIMARY KEY(id));"
                """.format(self._TABLE_NAME))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.create_table.__name__)
            self.close_conn()

    def add_website(self, user_id, website_name, website_link, website_keywords):
        try:
            self.curs.execute("""
                INSERT INTO {0} (user_id, name, link, keywords, create_date)
                values ('{0}', '{1}', '{2}', '{3}', '{4}');
                """.format(user_id, website_name, website_link, website_keywords, datetime.datetime.now()))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.add_website.__name__)
            self.close_conn()

    def get_websites(self, user_id):
        try:
            self.curs.execute("""
                SELECT * FROM {0}.{1}
                WHERE user_id = '{2}';
                """.format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id)
            )
        except Exception as e:
            self.error_print(e, __file__, self.get_websites.__name__)
            self.close_conn()
        return None if self.curs is None else self.curs.fetchall()

    def get_websites_with_search_word(self, user_id, search_word):
        if not search_word:
            return None
        try:
            self.curs.execute("""
                SELECT * FROM {0}.{1}
                WHERE user_id = '{2}'
                AND name LIKE '%{3}%';
                """.format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                search_word)
            )
        except Exception as e:
            self.error_print(e, __file__, self.get_websites.__name__)
            self.close_conn()
        return None if self.curs is None else self.curs.fetchall()

    def search_word_hit_count(self, user_id, search_word):
        if not search_word:
            return None
        websites = self.get_websites_with_search_word(user_id, search_word)
        hit_count = []
        try:
            for website in websites:
                html = requests.get(website["link"])
                # print("[hit_count] html_info\n{}".format(html.text))
                soup = BeautifulSoup(html.text, "lxml")
                body = soup.find("body").text
                hit_count.append(body.count(search_word))
        except Exception as e:
            self.error_print(e, __file__, self.search_word_hit_count.__name__)
            self.close_conn()
        return hit_count

    def get_website_title_with_link(self, link):
        if not link:
            return ""
        try:
            html = requests.get(link)
            # print("[title] html_info\n{}".format(html.text))
            soup = BeautifulSoup(html.text, "lxml")
            return soup.find("title").text
        except Exception as e:
            self.error_print(e, __file__, self.get_website_title_with_link.__name__)
            self.close_conn()

    def get_website_keywords_with_link(self, link):
        if not link:
            return ""
        try:
            html = requests.get(link)
            # print("[keywords] html_info\n{}".format(html.text))
            soup = BeautifulSoup(html.text, "lxml")
            return soup.find("meta", name="keywords").get("content", "")
        except Exception as e:
            self.error_print(e, __file__, self.get_website_keywords_with_link.__name__)
            self.close_conn()

    def delete_websites(self, user_id, delete_website_ids):
        copied_delete_website_ids = []
        if delete_website_ids and isinstance(delete_website_ids, list):
            copied_delete_website_ids = delete_website_ids.copy()
        try:
            self.curs.execute("""
                DELETE FROM {0}.{1}
                WHERE user_id = '{2}'
                AND _id IN ({3});
                """.format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                *copied_delete_website_ids)
            )
        except Exception as e:
            self.error_print(e, __file__, self.get_websites.__name__)
            self.close_conn()
