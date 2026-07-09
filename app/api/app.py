#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/6/1612:17
@Author  :shlongqishi@gmail.com
@File    :app.py
"""

"""
# 实例化封装类
# app = Http(__name__, conf=conf, db=db, router=injector.get(Router))  
# 这种写法，导致在代码中一直写全局变量，对代码不友好，应该使用依赖注入

# app = Http(__name__, router=injector.get(Router))   
*args:这个不需要。Python 仅允许形参位置写类型注解 变量: 类型，传参调用函数时绝对不能加 : 类型标注
"""
import dotenv
from flask_migrate import Migrate
from injector import Injector

from app.api.module import AppModule
from config import Config
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy_new import SQLAlchemy

dotenv.load_dotenv()

injector = Injector([AppModule])
"""Injector 读取 AppModule，它记住了：“以后谁要 SQLAlchemy，我就把 
database_extension.py 里那个唯一的全局 db 给他”"""
conf = Config()

# 从注入器获取 db 和 router（此时 db 应该是全局单例）
app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    migrate=injector.get(Migrate),
    router=injector.get(Router))
