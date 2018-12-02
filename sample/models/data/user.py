#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import datetime
from lib.bottle import Bottle
from sample.models.data import db
from sample import config


app = Bottle()


class User(db.DB):
    _TABLE_NAME = "user"

    def __init__(self):
        super(User, self).__init__()
        if not self.is_exist_table():
            self.create_table()

    def is_exist_table(self):
        try:
            self.curs.execute("""
                SELECT COUNT(*) FROM {0}
                WHERE TYPE='table' AND name='{1};'
                """.format(config.PROJECT_NAME, self._TABLE_NAME))
        except Exception as e:
            self.error_print(e, self.is_exist_table)
            self.close_conn()
        if self.curs.fetchone()[0] == 0:
            return False
        return True

    def create_table(self):
        try:
            self.curs.execute("""
                CREATE TABLE {}(
                _id int NOT NULL AUTO_INCREMENT,
                user_id int(20) NOT NULL,
                user_password varchar(20) NOT NULL,
                user_name varchar NOT NULL DEFAULT 'guest',
                create_date datetime NOT NULL,
                "PRIMARY KEY(id))"
                """.format(self._TABLE_NAME))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, self.create_table)
            self.close_conn()

    def confirm_user(self, user_id, user_password):
        try:
            self.curs.execute("""
                SELECT COUNT(*) FROM {0}.{1}
                WHERE user_id = '{2}'
                AND user_password = '{3}'
                """.format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                user_password)
            )
        except Exception as e:
            self.error_print(e, self.confirm_user)
            self.close_conn()
        if self.curs.fetchone()[0] == 0:
            return False
        return True

    def register_user(self, user_id, user_password):
        try:
            self.curs.execute("""
                INSERT INTO {0} (user_id, user_password, create_date)
                values ('{0}', '{1}', '{2}')
                """.format(user_id, user_password, datetime.datetime.now()))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, self.register_user)
            self.close_conn()

    def error_print(self, e, func):
        sys.stderr.write("{0}\n\tfile:{1}\n\tfunc:{2}".format(e, __file__, func.__name__))



