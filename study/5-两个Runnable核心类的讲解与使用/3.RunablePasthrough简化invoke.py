#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/814:32
@Author  :shlongqishi@gmail.com
@File    :2.RunnableParallel操作Runnable的输出.py
"""

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def retrieval(query: str) -> str:
    """"模拟一个检索其，传入查询query，输出文本"""
    print("执行检索：", query)
    return "我叫慕小课，是一名AI应用开发工程师"


# 1.编排Prompt
prompt = ChatPromptTemplate.from_template("""请根据用户的提问回答问题，可以参考对应的上下文进行回复。
<context>
{context}
<context>
用户的问题是：{query}""")  # 此处使用partial()的时候，尚未得到用户query的信息，所以无法实例化

# 2.构建大模型
llm = ChatOpenAI(model="deepseek-v4-flash")

# 3.创建输出解释器
parser = StrOutputParser()

# 4.编排链
# chain = prompt | llm | parser

# chain = RunnableParallel({
#     "context": lambda x: retrieval(x["query"]),
#     # "query": lambda x: x["query"],
#     "query": itemgetter("query"),  # itemgetter接收一个收入，类似lambda的简易写法
# }) | prompt | llm | parser

# 版本2：以下方案没有runnableParallel也能够运行，原因在于对应的数据转换为runnable
# 调整的时候注意是字典、列表、赋值，如果是字典前后需要对应
# chain = {
#             "context": lambda x: retrieval(x),  # x需要调用字典，所以x不能是字符串;前后保持一致即可
#             "query": lambda x: x,
#         } | prompt | llm | parser


# 版本3：通过字符串、runnablepassthrough函数来调用
chain = {
            # "context": lambda x: retrieval(x),  # x需要调用字典，所以x不能是字符串;前后保持一致即可
            "context": retrieval,
            "query": RunnablePassthrough(),  # 获取传递的数据  类型可以是字符串、字典等格式
        } | prompt | llm | parser

# RunnableParallel是每一个可运行的主键，并且可以通过管道来传输参数
# chain = RunnableParallel(
#     context=retrieval,
#     query=RunnablePassthrough(),
# ) | prompt | llm | parser


# 5.调用链生成结果
# content = chain.invoke({"context": retrieval("你好，我是谁？"), "query": "你好，我是谁？"})
# 以上模式中，用户提问书写两次，维护麻烦，所以会构造  定义检索函数retrieval()来构造一段上下文
# 如果没有context字典的话，会报错

# content = chain.invoke({"query": "你好，我叫什么？"})
# 版本3：
# content = chain.invoke("你好，我叫什么？")

# 版本3
# 4.构建链
chain = RunnablePassthrough.assign(context=lambda x: retrieval(x["query"])) | prompt | llm | parser
# RunnablePassthrough必须是一个字典

content = chain.invoke({"query": "你好，我是谁？"})

print(content)
