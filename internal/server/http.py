#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/6/1612:12
@Author  :shlongqishi@gmail.com
@File    :http.py
"""

import os

from flask import Flask
from flask_migrate import Migrate
from injector import inject

from config import Config
from internal.exception import CustomException
from internal.router import Router
from pkg.response import HttpCode, Response, json
from pkg.sqlalchemy_new import SQLAlchemy


@inject
class Http(Flask):
    """Http服务引擎"""
    """args非命名参数，kwargs命名参数"""

    def __init__(
            self,
            *args,
            conf: Config,
            db: SQLAlchemy,
            migrate: Migrate,
            router: Router,
            **kwargs):
        # 1.调用父类构造函数初始化
        super().__init__(*args, **kwargs)  # super的括号少了，kwargs的两个星号

        # 2.初始化应用配置
        self.config.from_object(conf)  # 调用父类的配置信息进行从对象获取

        # 3.注册绑定异常错误处理
        """raise后面只能跟exception的实例内容
        注册全局异常拦截后，所有接口抛出的业务异常，全部在一处统一序列化为
        JSON，不用每个接口重复写格式化代码。
        """
        self.register_error_handler(Exception, self._register_error_handler)

        # 4.初始化flask扩展，直接就是flask的应用，用self
        db.init_app(self)
        migrate.init_app(self, db, directory="internal/migration")  # 大部分扩展都可以调用init_app来实现实例化
        """flask-SQLAlchemy标准初始化，把db数据库实例绑定到flask应用self，完成关联"""

        # 避免自动创建数据库，所以要删除
        """
        with self.app_context(): # context是什么意思，也没有创建过这个函数？
            # flask运行需要应用上下文环境，保存当前应用、数据库连接、全局变量
            # 正常发送HTTP请求时，框架自动创建上下文。
            # 代码写在__init__启动阶段，没有请求触发上下文，需要手动临时创建环境
            # print("Http层db id =", id(db))
            #
        from internal.extension.database_extension import db as global_db
            # print("全局单例db id =", id(global_db))
            # print("两者是否相等：", db is global_db)
            # print("Database URI:", self.config.get('SQLALCHEMY_DATABASE_URI')) # 检查数据库的连接情况
            _ = App() # 这么做的目的是?

            # 只导入、实例化一次APP模型，不接受变量、数据库
            # 作用：强制python加载APP这个Model类
            
            db.create_all()  # 这个create_all()也是model的模板函数么？具体做什么操作？
            
            # 如果没有context上下文的话会直接报错
            # 属于SQLAlcehmy实例的顶层方法
            # 执行逻辑：
            # 1-进入上下文，建立数据库连接
            # 2-扫描加载、继承db.model的类APP
            # 3-自动根据类内Clomn生成CREATE_TABLE SQL
        """

        # 5.注册应用路由
        router.register_router(self)

    def _register_error_handler(self, error: Exception):
        # 1.如果异常信息是我们自定义的异常信息，就用message、data、code进行提取
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {},
            ))
        if self.debug or os.getenv("FLASK_ENV") == "development":
            raise error
        else:
            # 2.如果不是的话，就把error的信息提取出来
            return json(Response(
                code=HttpCode.FAIL,
                message=str(error),
                data={},
            ))
