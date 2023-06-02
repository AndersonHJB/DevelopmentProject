# # -*- coding: utf-8 -*-
# # @Time    : 2023/6/2 14:04
# # @Author  : AI悦创
# # @FileName: models.py.py
# # @Software: PyCharm
# # @Blog    ：https://bornforthis.cn/
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
#
#
# class Admin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#
#
# class Password(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     password = db.Column(db.String(80), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     valid_days = db.Column(db.Integer, nullable=False)  # 如果是永久密码，设为-1
from datetime import datetime


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Password:
    def __init__(self, password, created_at, valid_days):
        self.password = password
        self.created_at = created_at
        self.valid_days = valid_days


# class EncryptedContent:
#     def __init__(self, content):
#         self.content = content
