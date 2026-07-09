#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/809:40
@Author  :shlongqishi@gmail.com
@File    :2.LECL表达式简化版本.py
"""

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# 1.定义组件，prompt的输出是llm的输入，llm的输入是parser的输出，避免嵌套需要一个链式结构
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="deepseek-v4-flash")
parser = StrOutputParser()

# 2.简化版本的使用runnable结构
chain = prompt | llm | parser

# 3.调用链得到结果
print(chain.invoke({"query": "请讲一个程序员的冷笑话"}))
