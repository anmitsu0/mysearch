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

    def __del__(self):
        super(User, self).__del__()

    def create_table(self):
        try:
            self.curs.execute((
                "CREATE TABLE {0}.{1} ("
                "_id int NOT NULL AUTO_INCREMENT, "
                "id varchar(20) NOT NULL, "
                "password varchar(20) NOT NULL, "
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
            return bool(self.curs.fetchall())
        except Exception as e:
            self.error_print(e, __file__, self.confirm_user.__name__)
            return False

    def confirm_user_id(self, user_id):
        try:
            self.curs.execute((
                "SELECT * FROM {0}.{1} "
                "WHERE id = '{2}';"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
            ))
            return bool(self.curs.fetchall())
        except Exception as e:
            self.error_print(e, __file__, self.confirm_user.__name__)
            return False

    def register_user(self, user_id, user_password):
        # TODO: check: rename user_id
        try:
            self.curs.execute((
                "INSERT INTO {0}.{1} (id, password) "
                "VALUES ('{2}', '{3}');"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                user_id,
                user_password,
            ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.register_user.__name__)
            self.conn.rollback()

    def delete_users(self, delete_user_ids):
        # delete_user_ids: not list(_id) but list(user_id)
        copied_delete_user_ids = []
        if delete_user_ids and isinstance(delete_user_ids, list):
            copied_delete_user_ids = delete_user_ids.copy()
        try:
            for user_id in copied_delete_user_ids:
                self.curs.execute((
                    "DELETE FROM {0}.{1} "
                    "WHERE id = '{2}';"
                ).format(
                    config.PROJECT_NAME,
                    self._TABLE_NAME,
                    user_id
                ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.delete_users.__name__)
            self.conn.rollback()

    def get_users(self):
        try:
            self.curs.execute((
                "SELECT * FROM {0}.{1};"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME
            ))
            return self.curs.fetchall()
        except Exception as e:
            self.error_print(e, __file__, self.get_users.__name__)
            return None

    def update_password(self, user_id, current_password, new_password):
        try:
            self.curs.execute((
                "UPDATE {0}.{1} SET "
                "password = '{2}' "
                "WHERE id = '{3}' "
                "AND password = '{4}';"
            ).format(
                config.PROJECT_NAME,
                self._TABLE_NAME,
                new_password,
                user_id,
                current_password
            ))
            self.conn.commit()
        except Exception as e:
            self.error_print(e, __file__, self.update_password.__name__)
            self.conn.rollback()
