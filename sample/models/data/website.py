#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
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
                outline varchar NOT NULL,
                most_frequent_word varchar,
                create_date datetime NOT NULL,
                PRIMARY KEY(id));"
                """.format(self._TABLE_NAME))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.create_table.__name__)
            self.close_conn()

    def register_website(self, user_id, website_name, website_link, website_outline):
        try:
            self.curs.execute("""
                INSERT INTO {0} (user_id, name, link, outline, create_date)
                values ('{0}', '{1}', '{2}', '{3}', '{4}');
                """.format(user_id, website_name, website_link, website_outline, datetime.datetime.now()))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.register_website.__name__)
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
        return self.curs.fetchall()

    def get_websites_with_search_word(self, user_id, search_word):
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
        return self.curs.fetchall()

    def search_word_relevance(self, user_id, search_word):
        # TODO: need web scraping
        # returns: list(tuple(_id, 〇〇%))
        pass

    def search_word_hit_count(self, user_id, search_word):
        try:
            self.curs.execute("""
                SELECT *, COUNT(*) FROM {0}.{1}
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
        return (item["_id"] for item in self.curs.fetchall())

    def delete_website(self, user_id, delete_website_ids):
        new_delete_website_ids = []
        if delete_website_ids and isinstance(delete_website_ids, list):
            new_delete_website_ids = delete_website_ids[:]
        try:
            self.curs.execute("""
                DELETE FROM {0}.{1}
                WHERE user_id = '{2}'
                AND _id IN ({3});
                """.format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                *new_delete_website_ids)
            )
        except Exception as e:
            self.error_print(e, __file__, self.get_websites.__name__)
            self.close_conn()
