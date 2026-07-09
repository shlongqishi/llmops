#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/203:40
@Author  :shlongqishi@gmail.com
@File    :module.py
"""
from flask_migrate import Migrate
# api/module.py
from injector import Module, Binder, singleton

from internal.extension.database_extension import db
from internal.extension.migrate_extension import migrate
from internal.handler import AppHandler
from internal.router import Router
from pkg.sqlalchemy_new import SQLAlchemy


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # 将 SQLAlchemy 绑定到全局 db 实例，并声明为单例
        binder.bind(SQLAlchemy, to=db, scope=singleton)
        binder.bind(Router, to=Router, scope=singleton)
        binder.bind(AppHandler, to=AppHandler, scope=singleton)
        binder.bind(Migrate, to=migrate, scope=singleton)
