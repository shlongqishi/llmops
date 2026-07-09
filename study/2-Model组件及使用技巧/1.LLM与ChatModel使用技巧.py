#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/714:46
@Author  :shlongqishi@gmail.com
@File    :1.LLM与ChatModel使用技巧.py
"""
from datetime import datetime

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.编排prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请回答用户的额问题，现在的时间是{now}"),
    ("human", "{query}"),
]).partial(now=datetime.now())

# 2.创建大语言模型
llm = ChatOpenAI(model="deepseek-v4-flash")

ai_message = llm.invoke(prompt.invoke({"query": "现在是几点，请讲一个程序员的冷笑话"}))

print(ai_message)
print("===========================================")
print(ai_message.type)  # type类型输出为ai？这是什么意思？
print(ai_message.content)
print(ai_message.response_metadata)
