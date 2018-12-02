#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import mysql.connector
from lib.bottle import Bottle
from sample import config


app = Bottle()


class DB(object):
    _DATABASE = None

    def __init__(self):
        self.conn = self.get_conn()
        self.curs = self.conn.cursor(buffered=True)

    def get_conn(self):
        if self._DATABASE is None:
            self.conn = self._DATABASE = mysql.connector.connect(**config.DB_INFO[config.PROJECT_ENV])
        return self.conn

    def close_conn(self):
        if self._DATABASE is not None:
            self.conn.close()

    def is_exist_table(self):
        pass

    def create_table(self):
        pass
