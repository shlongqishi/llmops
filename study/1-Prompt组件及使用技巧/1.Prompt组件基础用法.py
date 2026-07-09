#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/617:16
@Author  :shlongqishi@gmail.com
@File    :1.Prompt组件基础用法.py
"""
from datetime import datetime

from langchain_core.messages import AIMessage
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder, HumanMessagePromptTemplate,
)

prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
print(prompt.format(subject="喜剧演员"))  # 底层使用f-string进行格式化
print(prompt.invoke({"subject": "程序员"}))  # 生成的是某一个值，通过ctrl+字段能够查看对应的入参值类型
prompt_value = prompt.invoke({"subject": "程序员"})
print(prompt_value.to_string())
print(prompt_value.to_messages())
print(i for i in prompt_value.to_messages())

print("=================================")
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据用户的提问进行回复，当前的时间为：{now}"),
    # 有时候需要其他的消息，暂时不确定的话可以先用占位符进行占位处理
    MessagesPlaceholder("chat_history"),  # 传递的是最终的消息，不可以带有变量
    HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话"),
]).partial(now=datetime.now())

chat_prompt_value = chat_prompt.invoke({
    # "now": datetime.now(),
    "chat_history": [
        ("human", "我叫慕小课"),
        AIMessage("你好，我是ChatGpt,有什么可以帮到他？")
    ],
    "subject": "程序员",
})
print(chat_prompt_value)
print(chat_prompt_value.to_string())  # 将信息转换为字符串
