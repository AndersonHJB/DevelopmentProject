# -*- coding: utf-8 -*-
# @Time    : 2023/6/11 22:26
# @Author  : AI悦创
# @FileName: database.py.py
# @Software: PyCharm
# @Blog    ：https://bornforthis.cn/
import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS chat
                        (username text, friend text, msg text, time text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                        (username text, password text)''')

    def insert_msg(self, username, friend, msg, time):
        self.c.execute("INSERT INTO chat VALUES (?, ?, ?, ?)", (username, friend, msg, time))
        self.conn.commit()

    def insert_user(self, username, password):
        self.c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        self.conn.commit()

    def query_user(self, username, password):
        self.c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.c.fetchone()

    def close(self):
        self.conn.close()
