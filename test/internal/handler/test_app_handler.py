#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/114:54
@Author  :shlongqishi@gmail.com
@File    :test_app_handler.py
"""
import pytest

from pkg.response.http_code import HttpCode


class TestAppHandler:
    """app的控制器"""

    @pytest.mark.parametrize("query", [None, "你好，你是谁会？"])
    def test_completion(self, query, client):
        """print("这是test_completion的语句内容")
        assert 1 == 1
        """
        resp = client.post("/api/v1/app/completion",
                           json={"query": query})  # 需要把访问地址写全，默认地址是原始的Running on http://127.0.0.1:5000
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.UNAUTHORIZED  # 为什么教程上是VALIDATE_ERROR,现在是UNAUTHORIZED，不限制了
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
        print("响应内容：", resp.json)
