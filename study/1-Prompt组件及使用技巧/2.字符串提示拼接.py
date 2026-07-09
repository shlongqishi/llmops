#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/618:01
@Author  :shlongqishi@gmail.com
@File    :2.字符串提示拼接.py
"""
from langchain_core.prompts import PromptTemplate

prompt = (
    # "你是谁啊？能这么干么？" +  第一个不能是字符串，必须是模板本身
        PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
        + "，让我开心下" +
        "\n使用{language}的语言"
)

print(prompt.invoke({"subject": "程序员", "language": "中文"}).to_string())
