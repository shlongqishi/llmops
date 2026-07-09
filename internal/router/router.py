#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/6/1518:48
@Author  :shlongqishi@gmail.com
@File    :router.py
"""
from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import AppHandler


@inject
@dataclass
class Router:
    """路由"""
    app_handler: AppHandler

    def register_router(self, app: Flask):
        """注册路由"""
        print("===== 路由注册函数执行成功 =====")
        # 1.创建一个蓝图
        # bp = Blueprint(name:"llmops", __name__, url_prefix="")  写法是错误的，调用函数的时候不需要类型注释
        bp = Blueprint(import_name=__name__, name="llmops",
                       url_prefix="/api/v1")  # 浏览器的访问链接需要为：http://127.0.0.1:5000/api/v1/ping

        # 2.将url与对应的控制器方法做绑定
        # bp.add_url_rule(rule:"/ping", methods=['GET','POST','DELETE'])
        # bp.add_url_rule(rule:"/ping", view_func=self.app_handler.ping) 写错了只允许在函数定义的时候做类型注解，调用函数传参的时候使用  变量=值
        #    bp.add_url_rule(rule="/ping", view_func=self.app_handler.ping)
        bp.add_url_rule(rule="/app/<uuid:app_id>/debug", methods=["POST"], view_func=self.app_handler.debug)

        """在app_handler创建create_app之后在router中进行绑定？这个是什么意思，包括这个板块的blueprint是做什么用的？"""
        # bp.add_url_rule(rule="/app", methods=["POST"], view_func=self.app_handler.create_app)
        """以上操作完还不能看到对应的表，需要创建表之后才可以"""
        # 查询对应的数据
        # bp.add_url_rule("/app/<uuid:id>", view_func=self.app_handler.get_app)

        # bp.add_url_rule("/app/<uuid:id>", methods=["POST"], view_func=self.app_handler.update_app)

        # bp.add_url_rule("/app/<uuid:id>/delete", methods=["POST"], view_func=self.app_handler.delete_app)
        # 3.在应用上注册蓝图
        app.register_blueprint(bp)
        # 仅主app才有url_map，打印全部已注册路由
        print("主Flask全部路由：", [rule.rule for rule in app.url_map.iter_rules()])

    """
         # 必须要要构造函数来做，多个注入的话使用dataclasses来批量注入,不需要单独构造
         def __init__(self, app_handler, AppHandler):
             self.app_handler = app_handler
     """
