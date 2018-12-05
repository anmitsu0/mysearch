#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import mysql.connector
from lib.bottle import Bottle
from sample import config


app = Bottle()


class DB(object):
    _DATABASE = None

    def __init__(self):
        self.conn = self.get_conn()
        self.curs = self.conn.cursor(buffered=True, dictionary=True)

    def get_conn(self):
        if self._DATABASE is None:
            self.conn = self._DATABASE = mysql.connector.connect(**config.DB_INFO[config.PROJECT_ENV])
        return self.conn

    def close_conn(self):
        if self._DATABASE is not None:
            self.conn.close()

    def is_exist_table(self, table_name):
        try:
            self.curs.execute("""
                SELECT * FROM {0}
                WHERE TYPE='table' AND name='{1}';
                """.format(config.PROJECT_NAME, table_name))
        except Exception as e:
            self.error_print(e, __file__, self.is_exist_table.__name__)
            self.close_conn()
        if self.curs is None:
            return False
        return True

    def create_table(self):
        pass

    def error_print(self, e, file_name, func_name):
        sys.stderr.write("{0}\n\tfile:{1}\n\tfunc:{2}".format(e, file_name, func_name))
