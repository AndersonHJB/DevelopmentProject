# -*- coding: utf-8 -*-
# @Time    : 2023/6/11 22:27
# @Author  : AI悦创
# @FileName: server.py.py
# @Software: PyCharm
# @Blog    ：https://bornforthis.cn/
import socket
from database import Database

s = socket.socket()
host = 'localhost'
port = 8088

s.bind((host, port))
s.listen(5)

db = Database('chat.db')

while True:
    c, addr = s.accept()
    print('连接地址', addr)
    c.send('欢迎连接'.encode('utf-8'))
    msg = c.recv(1024).decode()
    # 假设收到的消息格式为"username:friend:message"
    username, friend, message = msg.split(":")
    db.insert_msg(username, friend, message, '2023-01-01 10:00:00')
    c.close()

db.close()
