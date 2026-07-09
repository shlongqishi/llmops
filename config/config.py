#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/6/3000:01
@Author  :shlongqishi@gmail.com
@File    :config.py
"""
import os
from typing import Any

from .default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:  # 类型注释更方便前后对齐，输出Any不限制，因为env环境大部分是str
    return os.getenv(key, DEFAULT_CONFIG.get(key))  # 为了提升代码健壮性，设置第二参数为默认值


# 写个bool值型的配置项意义是什么呢？
def _get_bool(key: str) -> bool:
    """从环境变量中找获取布尔值型的配置项，找不到的话就返回默认值"""
    value: str = _get_env(key)
    return str(value).lower() == "true" if value is not None else False


class Config:
    def __init__(self):
        # 将wtf的csrf功能关闭
        # self.WTF_CSRF_ENABLED = False  # 也调整下模块，不需要硬编码
        self.WTF_CSRF_ENABLED = _get_bool("WTF_CSRF_ENABLED")

        # 配置数据库配置内容
        self.SQLALCHEMY_DATABASE_URI = _get_env("SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(_get_env("SQLALCHEMY_POOL_SIZE")),  # int数据，不是str
            "pool_recycle": int(_get_env("SQLALCHEMY_POOL_SIZE")),
        }  # 为什么这两个属性会封装到options中去，而url不会呢？是为了打包处理？理论上单独放出来更合理
        self.SQLALCHEMY_ECHO = _get_env("SQLALCHEMY_ECHO")
        """以上配置数据库配置内容全是硬编码，不符合工业化编程逻辑。因为后续要修改的话各个文件都要兼顾。
        理论上就做各种函数、类模块来打包，统一在env环境中配置、修改，其他地方仅供使用"""

        """通过函数
        _get_env、_get_bool等函数模块化后，直接调用从env中获取配置项。其中包括默认配置项
        然后利用FLASKSQLALchemy的扩展+配置连通到数据库中
        extension存放所有的扩展，然后开始整理扩展信息"""
