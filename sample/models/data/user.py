#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
from lib.bottle import Bottle
from sample.models.data import db
from sample import config


app = Bottle()


class User(db.DB):
    _TABLE_NAME = "user"

    def __init__(self):
        super(User, self).__init__()
        if not self.is_exist_table(self._TABLE_NAME):
            self.create_table()

    def create_table(self):
        try:
            self.curs.execute("""
                CREATE TABLE {}(
                _id int NOT NULL AUTO_INCREMENT,
                id varchar(20) NOT NULL,
                password varchar(20) NOT NULL,
                create_date datetime NOT NULL,
                PRIMARY KEY(id));"
                """.format(self._TABLE_NAME))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.create_table.__name__)
            self.close_conn()

    def confirm_user(self, user_id, user_password):
        try:
            self.curs.execute("""
                SELECT COUNT(*) FROM {0}.{1}
                WHERE id = '{2}'
                AND password = '{3}';
                """.format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                user_password)
            )
        except Exception as e:
            self.error_print(e, __file__, self.confirm_user.__name__)
            self.close_conn()
        if self.curs.fetchone()[0] == 0:
            return False
        return True

    def register_user(self, user_id, user_password):
        try:
            self.curs.execute("""
                INSERT INTO {0} (id, password, create_date)
                values ('{0}', '{1}', '{2}');
                """.format(user_id, user_password, datetime.datetime.now()))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.register_user.__name__)
            self.close_conn()
    
    def delete_users(self, delete_user_ids):
        copied_delete_user_ids = []
        if delete_user_ids and isinstance(delete_user_ids, list):
            copied_delete_user_ids = delete_user_ids.copy()
        try:
            self.curs.execute("""
                DELETE FROM {0}.{1}
                WHERE _id IN ({2});
                """.format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                *copied_delete_user_ids)
            )
        except Exception as e:
            self.error_print(e, __file__, self.delete_users.__name__)
            self.close_conn()

    def get_users(self):
        try:
            self.curs.execute("""
                SELECT * FROM {0}.{1};
                """.format(
                config.PROJECT_NAME,
                self._TABLE_NAME)
            )
        except Exception as e:
            self.error_print(e, __file__, self.get_users.__name__)
            self.close_conn()
        return self.curs.fetchall()
