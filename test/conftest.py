#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/115:24
@Author  :shlongqishi@gmail.com
@File    :conftest.py
"""
import pytest

from app.api.app import app
from internal.router import Router
from internal.handler.app_handler import AppHandler


@pytest.fixture
def client():
    """获取flask应用的测试应用，并返回对应的参数内容"""
    
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
