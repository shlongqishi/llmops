#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/216:57
@Author  :shlongqishi@gmail.com
@File    :app.py
"""
import uuid  # uuid是什么意思？
from datetime import datetime

from sqlalchemy import (
    Column, UUID, String, Text, DateTime,
    Index, PrimaryKeyConstraint,
)

from internal.extension.database_extension import db


class App(db.Model):  # 这里的Model到底是什么内容？引入db是数据库，通过类创建具体字段？
    """db是SQLAlchemy（）创建的数据库实例，db.Model是SQLAlchemy提供的基础映射父类
    模型继承db.model，orm识别为数据库表映射类
    底层Model封装了表创建、增删改查、字段映射、事务、关联查询全部逻辑
    Model是ORM表的模板父类，继承之后python才能映射成数据库表"""
    """AI应用基础模型类"""
    __tablename__ = "app"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_app_id"),  # id作为主键，name为主键的名称
        Index("idx_app_account_id", "account_id"),  # account_id作为索引，账号的索引约束  加快索引速度
    )

    id = Column(UUID, default=uuid.uuid4, nullable=False)  # 这里的uuid4是什么意思？
    """uuid全局唯一标识符，自增
    column是定义库表列信息
    uuid.uuid4()生成随机型UUID，完全随机生成，业务主键最常使用
    uuid1、uuid3、uuid4、uuid5是代表生成的逻辑"""
    account_id = Column(UUID, nullable=False)
    name = Column(String(255), default="", nullable=False)  # 255的时候性能会下降？为什么？
    """不会性能下降，255是数据库里是最有通用长度
    超过255的字符串建议使用Text，255以内是1字节长度"""
    icon = Column(String(255), default="", nullable=False)
    description = Column(Text, default="", nullable=False)  # 描述存储的数据比较长，可以存长内容
    status = Column(String(255), default="", nullable=False)  # 迁移新增的字段
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # 记录的更新时间
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # datetime.now函数调用，但是调用now()函数
    """now()程序调用瞬间执行一次，生成固定时间戳
    函数本身now的话每次插入新记录会自动调用获取当前实时时间"""
