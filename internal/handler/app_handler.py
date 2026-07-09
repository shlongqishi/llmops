#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/6/1518:36
@Author  :shlongqishi@gmail.com
@File    :app_handler.py
"""
import uuid
from dataclasses import dataclass
from uuid import UUID

from flask import jsonify
from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器，路由的时候优先进行控制器调用"""
    app_service: AppService
    """"这个app_handler文件有什么做什么？每次创建数据库、调用接口包括completion函数也在这里？这么区分的目的是什么？
    接口入口层，只负责处理HTTP请求，不碰数据库、不实现业务逻辑
    1-接收、校验前端传参【按到get、post等请求数据，不进业务逻辑】
    2-调用service层执行业务【数据库创建、ai对话、复杂计算交给AppSevice，Handler只做转发】
    3-统一封装返回格式【success_json标准化接口返回JSON，统一响应结构】
    handler只做---请求》校验》调服务》封装返回---的中转，不写核心逻辑
    """

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经成功创建，id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是：{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id为{app.id}")

    def debug(self, app_id: UUID):
        """"聊天窗口"""
        # 1.提取从接口获取的输入，post get delete方法
        # 获取请求后进行校验
        req = CompletionReq()
        if not req.validate():
            # return req.errors
            return validate_json(req.errors)

        # query = request.json.get("query")   #没有封装completionReq时的调用

        # 2.构建组件
        prompt = ChatPromptTemplate.from_template("{query}")
        llm = ChatOpenAI(model="deepseek-v4-flash")
        parser = StrOutputParser()

        # 3.构建链
        chain = prompt | llm | parser

        # 4.调用链得到结果
        content = chain.invoke({"query": req.query.data})  # 这里是参数不是直接的语句内容

        """
        # 2.创建大模型的代理模块，构建openai客户端，并发起请求
        llm = ChatOpenAI(model="deepseek-v4-flash")

                client = OpenAI(
                    api_key=os.environ.get('DEEPSEEK_API_KEY'),  # DS的密钥为："sk-3adff6659a95495c9fbd60e71c686943",
                    base_url="https://api.deepseek.com")
                
                client = OpenAI(
                    base_url=os.getenv('OPENAI_BASE_URL')  # 使用os.getenv的时候必须默认使用OPENAI 而不能使用DEEPSEEK
                )
        
        # 3.通过代理模块调用大模型进行补全对话【得到请求响应，然后将openai的响应传输至前端】
        ai_message = llm.invoke(prompt.invoke({"query": req.query.data}))

        parser = StrOutputParser()
                            
                            completion = client.chat.completions.create(
                                model="deepseek-v4-flash",
                                messages=[
                                    {"role": "system", "content": "你是OpenAI开发聊天机器人，请根据用户的输入回复对应的信息"},
                                    {"role": "user", "content": req.query.data},
                                ])
                    
                            content = completion.choices[0].message.content
                            
                            resp = Response(code=HttpCode.SUCCESS, message="", data={"content": content, })
                            # resp不能直接打印出来，因为flask中只接受字典、str、或者序列化后的字典
                            # 通过在response模块中封装语句，将response变得简单化，具体就是通过函数来调用值
                            return jsonify(resp), 200
                            
        """
        # 4.利用输出解析器输出对应的内容【解析响应内容】
        # content = parser.invoke(ai_message)
        return success_json({"content": content})

    def ping(self):
        return jsonify(FailException("数据未找到"))
        print("===== ping接口被调用 =====")
        return {"code": 0, "msg": "pong"}
