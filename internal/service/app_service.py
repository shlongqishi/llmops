# ! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/311:44
@Author  :shlongqishi@gmail.com
@File    :app_service.py
"""
import uuid
from dataclasses import dataclass

from injector import inject

from internal.model.app import App
from pkg.sqlalchemy_new import SQLAlchemy

""" 最困惑的是数据库表的内容定义是在model中，但是生成、提交是在service文件夹下，为什么这么设置呢？或者设置的依据是什么呢？
按照工程标准MVC、DDD领域渠道设计分层来划分，表定义model，增删改查在service
model层：定义数据库表接口、字段、约束、orm映射关系
service层：业务数据、事务交互、业务组合。完整办事流程----业务逻辑
领域模型model存放数据实体，应用服务service承载数据实体
"""

""""inject解释
依赖注入@inject思路：外部把需要的资源提前造好，自动传输给服务，服务只管声明需要什么，不用自己创建。
类直接申明db:SQLAlchemy   容器自动匹配对应实例赋值
解耦：service不关心db怎么初始化，只使用
单元测试：测试时注入mock的db，不用联真实数据库
统一全局资源（db、路由、缓存、oss）
省去人工多层级手动传递实例的转包流程，依赖由容器自动递归装配；新增 / 删除依赖时，只需要在对应类内部声明，上层、中间调用链路完全不用改动。
1-环境隔离：开发 / 测试环境一键替换依赖，测试时绑定 MockDB，业务代码完全不用修改；手动传参需要所有实例化处手动替换。
2-全局单例管控：db、redis 这类资源只初始化一次，容器统一单例管理，不会多处重复创建数据库连接
"""

"""dataclass解释
自动生成构造函数，不用手动写 __init__(self)的构造函数
@dataclass自动根据类上声明的类型字段，自动生成构造函数，省去手写__init__
也能自动实现__repr__、__eq__这些函数
类字段db:SQLAlchemy=依赖参数，自动生成构造函数接收db
"""


@inject  # 注入到底怎么理解？感觉每次都不是很   清楚？
@dataclass  # 构造函数模板？是不是类似的钩子函数不用写了
class AppService:
    """应用服务逻辑"""
    db: SQLAlchemy  # 这个只声明类型就行？不需要赋值或者怎么样？好奇怪
    """@dataclass语法规则===中约定   类变量只写  变量：类型 代表  构造函数入参  不需要手动赋值，dataclass自动赋值给self.db
    @inject容器自动注入赋值===项目启动时一来容器已经实例化全局db对象，通过injector.get(AppService)获取服务时，
    自动把db实力传入构造函数，最终self.db就是SQLAlchemy对象"""

    def create_app(self) -> App:
        with self.db.auto_commit():
            # 1.创建模型的实体类
            app = App(name="测试机器人", account_id=uuid.uuid4(), icon="", description="这是一个简单的聊天机器人")
            """以下写法也可以，但是常用的是在以上定义中书写
            app.name = "测试机器人"
            app.icon = ""
            app.description = "这是一个简单的聊天机器人"
            """
            # 2.将实体类添加到session会话中
            self.db.session.add(app)
            """有自动提交的函数，就不需要以下操作
            # 3.提交session会话
            self.db.session.commit()
            """
        return app

    def get_app(self, id: uuid.UUID) -> App:
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "慕课聊天机器人"
            # self.db.session.commit()
        return app

    def delete_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
            # self.db.session.commit()
        return app
