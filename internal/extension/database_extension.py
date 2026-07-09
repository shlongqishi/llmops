#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/203:20
@Author  :shlongqishi@gmail.com
@File    :database_extension.py
"""
from pkg.sqlalchemy_new import SQLAlchemy

db = SQLAlchemy()  # 实例化内容
# db.init_app()  # 初始化数据库内容 # 括号需要传入flask的应用内容，也就是app.http.app，但是不符合依赖注入？
"""?依赖注入到底是什么？仔细理解之后，用大白话描述下：
层层递进的进行类型注释，避免实例一直要写，和dataclass一起使用效果更好   实例：类型
"""
