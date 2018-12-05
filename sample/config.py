#!/usr/bin/env python3
# -*- coding:utf-8 -*-


SECTION_NAME = 'sample'
PROJECT_NAME = "mysearch"
PROJECT_ENV = "local"
# PROJECT_ENV = "CentOS"

DB_INFO = dict()
DB_INFO["local"] = dict(
    port="3307",
    host="localhost",
    db="{}".format(PROJECT_NAME),
    user="root",
    passwd="Pep_1xx877Tth",
    charset="utf8"
)
DB_INFO["CentOS"] = dict(
    port="3306",
    host="localhost",
    db="{}".format(PROJECT_NAME),
    user="hoge",
    passwd="eagSLk9e2f",
    charset="utf8"
)

ADMIN_USER_INFO = dict(
    id="admin",
    password="q2Qyj2Fb2pubwlkbm3eb"
)
