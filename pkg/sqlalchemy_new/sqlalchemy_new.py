#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Time    : 2026/7/608:48
@Author  :shlongqishi@gmail.com
@File    :sqlalchemy.py
"""
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    """重新sqlalchemy的核心类，实现自动提交的功能"""

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
