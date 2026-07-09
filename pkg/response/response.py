#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/6/3009:49
@Author  :shlongqishi@gmail.com
@File    :response.py
"""
from dataclasses import field, dataclass
from multiprocessing.dummy import dict
from typing import Any

from flask import jsonify

from .http_code import HttpCode


@dataclass
class Response:
    """基础http响应格式约定"""
    code: HttpCode = HttpCode.SUCCESS
    message: str = ""
    data: Any = field(default_factory=dict)


def json(data: Response = None):
    # 通过json将response类输出的内容进行序列化===基础响应接口
    return jsonify(data), 200


def success_json(data: Any = None):
    # 调用response类先返回对应的内容，然后将成功的状态信息返回
    return json(Response(code=HttpCode.SUCCESS, message="", data=data))


def fail_json(data: Any = None):
    # 返回失败的状态信息
    return json(Response(code=HttpCode.FAIL, message="", data=data))


def unauthorized_json(data: Any = None):
    # 返回未授权的状态信息，将data中的数据呈现在message中
    return json(Response(code=HttpCode.UNAUTHORIZED, message="", data=data))


def forbidden_json(data: Any = None):
    # 返回禁止的状态信息
    return json(Response(code=HttpCode.FORBIDDEN, message="", data=data))


def validate_json(errors: dict = None):
    # 返回未授权的状态信息，将data中的数据呈现在message中
    first_key = next(iter(errors))
    if first_key is not None:
        msg = errors.get(first_key)[0]
    else:
        msg = ""
    return json(Response(code=HttpCode.UNAUTHORIZED, message=msg, data=errors))


def message(code: HttpCode = None, msg: str = ""):
    """基础消息响应，固定返回消息提示，数据固定为空字典"""
    return json(Response(code=code, message=msg, data={}))


def success_message(msg: str = ""):
    """成功的状态响应"""
    return message(code=HttpCode.SUCCESS, msg=msg)


def fail_message(msg: str = ""):
    """失败的状态响应"""
    return message(code=HttpCode.FAIL, msg=msg)


def unauthorized_message(msg: str = ""):
    """未授权的状态响应"""
    return message(code=HttpCode.UNAUTHORIZED, msg=msg)


def forbidden_message(msg: str = ""):
    """禁止的状态响应"""
    return message(code=HttpCode.FORBIDDEN, msg=msg)


def unfound_message(msg: str = ""):
    """没有找到对应的信息内容"""
    return message(code=HttpCode.UNFOUND, msg=msg)
