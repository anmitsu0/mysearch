#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from sample.models.data import db
from sample import config


class Website(db.DB):
    _TABLE_NAME = "website"

    def __init__(self):
        super(Website, self).__init__()
        if not self.is_exist_table(self._TABLE_NAME):
            self.create_table()

    def __del__(self):
        super(Website, self).__del__()

    def create_table(self):
        try:
            self.curs.execute((
                "CREATE TABLE {0}.{1} ("
                "_id int NOT NULL AUTO_INCREMENT, "
                "user_id varchar(20) NOT NULL, "
                "name varchar(500) NOT NULL, "
                "link varchar(2000) NOT NULL, "
                "keywords varchar(500) NOT NULL, "
                "most_frequent_word varchar(30) DEFAULT '', "
                "create_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, "
                "PRIMARY KEY(_id));"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME
            ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.create_table.__name__)
            self.conn.rollback()

    def add_website(self, user_id, website_name, website_link, website_keywords):
        # TODO: check: rename website_name
        try:
            self.curs.execute((
                "INSERT INTO {0}.{1} (user_id, name, link, keywords) "
                "VALUES ('{2}', '{3}', '{4}', '{5}');"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                website_name,
                website_link,
                website_keywords
            ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.add_website.__name__)
            self.conn.rollback()

    def get_websites(self, user_id):
        try:
            self.curs.execute((
                "SELECT * FROM {0}.{1} "
                "WHERE user_id = '{2}';"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id
            ))
            return self.curs.fetchall()
        except Exception as e:
            self.error_print(e, __file__, self.get_websites.__name__)
            return []

    def search_word_hit_count(self, user_id, search_word):
        if not search_word:
            return []
        websites = self.get_websites(user_id)
        hit_count = []
        try:
            for website in websites:
                html = requests.get(website["link"])
                # print("[hit_count] html_info\n{}".format(html.text))
                soup = BeautifulSoup(html.text, "lxml")
                # body = soup.find("body").text if soup.find("body") else ""
                # hit_count.append(body.count(search_word))
                html_str = soup.prettify()
                hit_count.append(html_str.count(search_word))
        except Exception as e:
            self.error_print(e, __file__, self.search_word_hit_count.__name__)
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
            return ""

    def get_website_keywords_with_link(self, link):
        if not link:
            return ""
        try:
            html = requests.get(link)
            # print("[keywords] html_info\n{}".format(html.text))
            soup = BeautifulSoup(html.text, "lxml")
            meta_keyword = soup.find("meta", attrs={"name": "keywords", "content": True})
            return meta_keyword.get("content", "") if meta_keyword else ""
        except Exception as e:
            self.error_print(e, __file__, self.get_website_keywords_with_link.__name__)
            return ""

    def delete_websites(self, user_id, delete_website_ids):
        copied_delete_website_ids = []
        if delete_website_ids and isinstance(delete_website_ids, list):
            copied_delete_website_ids = delete_website_ids.copy()
        try:
            for _id in copied_delete_website_ids:
                self.curs.execute((
                    "DELETE FROM {0}.{1} "
                    "WHERE user_id = '{2}' "
                    "AND _id = '{3}';"
                ).format(
                    config.PROJECT_NAME,
                    self._TABLE_NAME,
                    user_id,
                    _id
                ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.get_websites.__name__)
            self.conn.rollback()

    def delete_websites_with_user_ids(self, delete_user_ids):
        copied_delete_user_ids = []
        if delete_user_ids and isinstance(delete_user_ids, list):
            copied_delete_user_ids = delete_user_ids.copy()
        try:
            for user_id in copied_delete_user_ids:
                self.curs.execute((
                    "DELETE FROM {0}.{1} "
                    "WHERE user_id = '{2}';"
                ).format(
                    config.PROJECT_NAME,
                    self._TABLE_NAME,
                    user_id
                ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.get_websites.__name__)
            self.conn.rollback()
