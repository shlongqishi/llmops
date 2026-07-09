#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/808:49
@Author  :shlongqishi@gmail.com
@File    :1. 手写Chain实现简易版本.py
"""
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# 1.定义组件，prompt的输出是llm的输入，llm的输入是parser的输出，避免嵌套需要一个链式结构
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="deepseek-v4-flash")
parser = StrOutputParser()


@dataclass
# 2.定义链模块
class Chain:
    steps: list
    """
    # 使用dataclass装饰器进行自动构造函数
    def __init__(self, steps: list):
        self.steps = steps
    """

    # 为什么需要invoke方法呢？直接使用其他的逻辑？
    def invoke(self, input: Any) -> Any:
        for step in self.steps:
            input = step.invoke(input)
            print("步骤：", step)
            print("输出：", input)
            print("-------------------")
        return input


# 3.输出链
chain = Chain([prompt, llm, parser])

# 4.调试链并输出结果
print(chain.invoke({"query": "你好，你是？"}))
