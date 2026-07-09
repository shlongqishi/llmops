#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/716:44
@Author  :shlongqishi@gmail.com
@File    :1-StrOutputParser使用技巧.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.创建大模型模板
prompt = ChatPromptTemplate.from_template("{query}")

# 2.创建大模型应用
llm = ChatOpenAI(model="deepseek-v4-flash")

# 3.创建大模型字符串输出解析器
parser = StrOutputParser()

# 4.应用大模型模板场景并应用输出解析器
content = parser.invoke(llm.invoke(prompt.invoke({"query": "你好，你是？"})))

print(content)
