#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime
from sample.models.data import db
from sample import config


class User(db.DB):
    _TABLE_NAME = "user"

    def __init__(self):
        super(User, self).__init__()
        if not self.is_exist_table(self._TABLE_NAME):
            self.create_table()

    def create_table(self):
        try:
            self.curs.execute((
                "CREATE TABLE {0}.{1} ("
                "_id int NOT NULL AUTO_INCREMENT, "
                "id varchar(20) NOT NULL, "
                "password varchar(20) NOT NULL, "
                "create_date datetime DEFAULT CURRENT_TIMESTAMP, "
                "PRIMARY KEY(_id));"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME
            ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.create_table.__name__)
            self.close_conn()

    def confirm_user(self, user_id, user_password):
        try:
            self.curs.execute((
                "SELECT * FROM {0}.{1} "
                "WHERE id = '{2}' "
                "AND password = '{3}';"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                user_password
            ))
        except Exception as e:
            self.error_print(e, __file__, self.confirm_user.__name__)
            self.close_conn()
        return bool(self.curs.fetchall())

    def register_user(self, user_id, user_password):
        try:
            self.curs.execute((
                "INSERT INTO {0}.{1} (id, password) "
                "values ('{2}', '{3}');"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                user_password,
            ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.register_user.__name__)
            self.close_conn()
    
    def delete_users(self, delete_user_ids):
        copied_delete_user_ids = []
        if delete_user_ids and isinstance(delete_user_ids, list):
            copied_delete_user_ids = delete_user_ids.copy()
        try:
            self.curs.execute((
                "DELETE FROM {0}.{1} "
                "WHERE _id IN ({2});"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                *copied_delete_user_ids
            ))
        except Exception as e:
            self.error_print(e, __file__, self.delete_users.__name__)
            self.close_conn()

    def get_users(self):
        try:
            self.curs.execute((
                "SELECT * FROM {0}.{1};"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME
            ))
        except Exception as e:
            self.error_print(e, __file__, self.get_users.__name__)
            self.close_conn()
        return self.curs.fetchall()
