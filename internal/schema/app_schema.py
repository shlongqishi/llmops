#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/6/2923:41
@Author  :shlongqishi@gmail.com
@File    :app_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    """基础聊天接口请求校验"""
    # 必填，长度最大为2000
    query = StringField("query", validators=[
        DataRequired(message="用户输入是必填的"),
        Length(max=2000, message="用户输入不超过2000字符")
    ])
