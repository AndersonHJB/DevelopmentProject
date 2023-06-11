# -*- coding: utf-8 -*-
# @Time    : 2023/6/11 22:28
# @Author  : AI悦创
# @FileName: main.py
# @Software: PyCharm
# @Blog    ：https://bornforthis.cn/
from database import Database

db = Database('chat.db')
db.insert_user('Alice', 'password123')
db.close()
