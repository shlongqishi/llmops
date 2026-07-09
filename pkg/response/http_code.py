#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/6/3009:44
@Author  :shlongqishi@gmail.com
@File    :http_code.py
"""
from enum import Enum


class HttpCode(str, Enum):  # 既是枚举也是字符串，不是单纯的元组字段
    """基础业务状态码，接口状态响应码，调用接口的时候回参中呈现的"""
    SUCCESS = "success"  # 成功状态
    FAIL = "fail"  # 失败状态
    UNFOUND = "unfound"  # 没有找到
    UNAUTHORIZED = "unauthorized"  # 未授权访问信息
    FORBIDDEN = "forbidden"  # 禁止访问信息，没有权限的意思
    VALIDATE_ERROR = "validate_error"  # 验证数据格式错误
