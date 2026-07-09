#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/811:00
@Author  :shlongqishi@gmail.com
@File    :1.RunnableParallel使用技巧.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()  # 这句语句的意思是什么？

# 1. 创建模型组件
joke_prompt = ChatPromptTemplate.from_template("请讲一个关于{subject}的笑话，尽可能短一点")
poem_prompt = ChatPromptTemplate.from_template("请讲一个关于{subject}的诗歌，尽可能短一点")

# 2. 创建大语言模型
llm = ChatOpenAI(model="deepseek-v4-flash")

# 3. 创建输出解释器
parser = StrOutputParser()

# 4. 使用lcel语法  编排链
joke_chain = joke_prompt | llm | parser
poem_chain = poem_prompt | llm | parser

# 5. 模型并行使用
map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

# map_chain = RunnableParallel({
#     "joke": joke_chain,
#     "poem": poem_chain,
# })

res = map_chain.invoke({"subject": "产品经理"})
print(res)
