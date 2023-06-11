# -*- coding: utf-8 -*-
# @Time    : 2023/6/11 22:27
# @Author  : AI悦创
# @FileName: client.py.py
# @Software: PyCharm
# @Blog    ：https://bornforthis.cn/
import socket
from tkinter import *
from database import Database
import matplotlib.pyplot as plt
import numpy as np


class Client:
    def __init__(self):
        self.db = Database('chat.db')
        self.root = Tk()
        self.root.geometry('300x300')
        self.username = Entry(self.root)
        self.password = Entry(self.root, show='*')
        self.login_btn = Button(self.root, text='登录', command=self.login)
        self.username.pack()
        self.password.pack()
        self.login_btn.pack()

    def login(self):
        username = self.username.get()
        password = self.password.get()
        if self.db.query_user(username, password) is not None:
            print('登录成功')
            # 打开聊天窗口等
            self.chat_win = Toplevel(self.root)
            self.chat_win.geometry('300x300')
            self.friend = Entry(self.chat_win)
            self.message = Entry(self.chat_win)
            self.send_btn = Button(self.chat_win, text='发送', command=self.send_msg)
            self.friend.pack()
            self.message.pack()
            self.send_btn.pack()
        else:
            print('用户名或密码错误')

    def send_msg(self):
        friend = self.friend.get()
        message = self.message.get()
        if message.startswith('plot:'):  # 如果消息以"plot:"开头，那么就画图
            func = message[5:]
            x = np.linspace(-10, 10, 100)
            y = eval(func)
            plt.figure()
            plt.plot(x, y)
            plt.title(func)
            plt.show()
        else:  # 否则就发送消息
            s = socket.socket()
            s.connect(('localhost', 12345))
            s.send(f'{self.username.get()}:{friend}:{message}'.encode())
            s.close()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    client = Client()
    client.run()
