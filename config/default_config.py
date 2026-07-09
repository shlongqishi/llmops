#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/203:02
@Author  :shlongqishi@gmail.com
@File    :default_config.py
"""
# 应用默认配置选项
DEFAULT_CONFIG = {
    # wtf的配置项
    "WTF_CSRF_ENABLED": False,
    """为什么env文件中使用=来赋值，但是config中就使用：来赋值呢？不同文件的约定是什么 """


    # SQLAlchemy数据库配置
    "SQLALCHEMY_DATABASE_URI": '',
    # 不能使用= ，而是用：，使用：代表的是字典，而不是赋值逻辑。所以提示不能赋值给字面量
    # 以上语句次序是数据库名称、账号、密码、地址、数据库具体哪个、编码模式
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECH0": 'TRUE',
}
