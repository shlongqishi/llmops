#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/109:39
@Author  :shlongqishi@gmail.com
@File    :exception.py
"""
from dataclasses import field
from typing import Any

from pkg.response.http_code import HttpCode


class CustomException(Exception):  # 继承exception不需要导入模块么？
    # 基础的异常信息披露
    code: HttpCode = HttpCode.FAIL
    message: str = ""
    data: Any = field(default_factory=dict)

    def __init__(self, message: str = "", data: Any = None):
        super().__init__()
        self.message = message
        self.data = data


def FailException(CustomExeception):
    """常规的异常信息"""
    pass


def NotFundException(CustomException):
    """未找到异常信息"""
    code = HttpCode.UNFOUND


def UnauthorizedException(CustomException):
    """未经授权的异常信息"""
    code = HttpCode.UNAUTHORIZED


def FobiddenException(CustomException):
    """授权禁止的异常信息"""
    code = HttpCode.FORBIDDEN


def ValidateErrorException(CustomException):
    """验证报错的异常信息"""
    code = HttpCode.VALIDATE_ERROR
