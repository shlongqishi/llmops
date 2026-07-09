#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/909:48
@Author  :shlongqishi@gmail.com
@File    :1.回调功能使用技巧.py
"""
import time
from typing import Any
from uuid import UUID

import dotenv
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class LLMOpsCallbackHandler(BaseCallbackHandler):
    """自定义llmops回调处理器，方便排查模块的问题"""
    start_at: float = 0

    def on_chat_model_start(
            self,
            serialized: dict[str, Any],  # 模型的配置信息，温度、配置等信息
            messages: list[list[BaseMessage]],  # 传输给函数的信息
            *,
            run_id: UUID,  # 主键信息
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            metadata: dict[str, Any] | None = None,
            **kwargs: Any,
    ) -> Any:
        print("聊天模型开始执行了")
        print("serialized:", serialized)
        print("message:", messages)
        self.start_at = time.time()

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            **kwargs: Any,
    ) -> Any:
        end_at: float = time.time()
        print("完整输出：", response)
        print("程序消耗：", end_at - self.start_at)


"""
    def on_llm_new_token(  # 只是一个函数，而不是类，在config中配置的时候只有类名
            self,
            token: str | list[str | dict[str, Any]],
            *,
            chunk: GenerationChunk | ChatGenerationChunk | None = None,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            **kwargs: Any,
    ) -> Any:
        print("token生成了")
        print("token:", token)
"""

# 1.编排Prompt
prompt = ChatPromptTemplate.from_template("""{query}""")

# 2.构建大模型
llm = ChatOpenAI(model="deepseek-v4-flash")

# 3.创建输出解释器
parser = StrOutputParser()

# 4.编排链
# 版本3：通过字符串、runnablepassthrough函数来调用
chain = {"query": RunnablePassthrough()} | prompt | llm | parser

# 4.调用链并执行
resp = chain.stream("你好，我是谁？",
                    config={"callbacks": [StdOutCallbackHandler(), LLMOpsCallbackHandler()]})  # 在语句内传输callbacks回调语句
# invoke是一次性生成新内容，不会逐渐展示token情况  stream模式下会展示

for chunk in resp:
    pass
