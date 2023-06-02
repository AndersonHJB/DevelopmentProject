import base64  # 导入base64库，用于对图像进行编码和解码
from time import time  # 导入time库的time函数，用于获取当前时间
from utlib import bao, meibai, quban  # 从utlib库中导入bao、meibai和quban模块
import cv2  # 导入cv2库，用于图像处理
import numpy as np  # 导入numpy库，用于处理数组
from flask import Flask, render_template, jsonify, request  # 导入flask库的相关模块

app = Flask(__name__)  # 实例化一个Flask应用


@app.route('/')  # 定义应用的根路由
def show():
    return render_template('show.html')  # 渲染并返回show.html模板


@app.route('/predict/', methods=['POST'])  # 定义预测路由，接受POST请求
def predict():
    # 获取从客户端传过来的原始图像数据
    file = request.form.get('data')  # 从POST请求中获取名为"data"的表单数据，这里是包含图像的base64编码字符串
    data_url = str.split(file, ',')[1]  # 将获取到的base64字符串按照逗号分割，取第二部分（实际的图像数据）
    img_data = base64.urlsafe_b64decode(
        data_url + '=' * (4 - len(data_url) % 4))  # 对图像数据进行base64解码，补全末尾的等号以满足base64解码要求
    img_data = np.frombuffer(img_data, np.uint8)  # 将解码后的图像数据转换为一个numpy数组，数组类型为无符号8位整数
    img_arr = cv2.imdecode(img_data, cv2.IMREAD_COLOR)  # 使用cv2.imdecode()函数将numpy数组解码为一个OpenCV图像对象，设置为彩色图像
    cv2.imwrite("./static/images/1.jpg", img_arr)  # 将解码后的图像保存到指定路径（"./static/images/1.jpg"）
    return jsonify({'action': '成功'})  # 返回处理结果的JSON数据


@app.route('/meibai/')  # 定义美白路由
def meibais():
    meibai.face_whitening()  # 调用meibai模块的face_whitening函数
    return jsonify({'path': './static/images/meibai.jpg'})  # 返回处理后的图像路径


@app.route('/quban/')  # 定义去斑路由
def qubans():
    quban.quban()  # 调用quban模块的quban函数
    return jsonify({'path': './static/images/quban.jpg'})  # 返回处理后的图像路径


@app.route('/bao/')  # 定义饱和度增强路由
def baos():
    bao.ColorEnhancement()  # 调用bao模块的ColorEnhancement函数
    return jsonify({'path': './static/images/bao.jpg'})  # 返回处理后的图像路径


@app.route('/mopi/')  # 定义磨皮路由
def mopis():
    quban.mopi()  # 调用quban模块的mopi函数
    return jsonify({'path': './static/images/mopi.jpg'})  # 返回处理后的图像路径


if __name__ == '__main__':
    app.run(port=5000)  # 运行应用，监听5000端口
    # 找到这个app，然后点击鼠标右键，找到run，然后点击
    # 最后点击出来的网址 http://127.0.0.1:5000
