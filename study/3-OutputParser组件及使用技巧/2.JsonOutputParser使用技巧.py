#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/717:04
@Author  :shlongqishi@gmail.com
@File    :2.JsonOutputParser使用技巧.py
"""
import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import Field, BaseModel

dotenv.load_dotenv()


# 1.创建一个json数据结构，用于告诉大语言模型这个json长什么样子
# langchain_core.pydantic_v1  BaseModel, Field  该模块已经失效了
class Joke(BaseModel):
    # 冷笑话
    joke: str = Field(description="回答用户的冷笑话")
    # 冷笑话的笑点
    punchline: str = Field(description="这个冷笑话的笑点")


parser = JsonOutputParser(pydantic_object=Joke)

# 2.构建一个提示模板
prompt = ChatPromptTemplate.from_template("请根据用户的提问进行回答。\n{format_instructions}\n{query}").partial(
    format_instructions=parser.get_format_instructions())

# print(parser.get_format_instructions())
print(prompt.format(query="请讲一个关于程序员的冷笑话"))
print("--------------------------------------------")

# 3.构建一个大模型
llm = ChatOpenAI(model="deepseek-v4-flash")

# 4.提示模板在大模型上的使用
content = parser.invoke(llm.invoke(prompt.invoke({"query": "请输出一个程序员的冷笑话"})))

print(type(content))
print(content.get("punchline"))
print(content)
