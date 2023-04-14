import base64
from time import time
from utlib import bao, meibai, quban
import cv2
import numpy as np
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def show():
    return render_template('show.html')


@app.route('/predict/', methods=['POST'])
def predict():
    # 获取传送过来的完整原始图像
    file = request.form.get('data')
    data_url = str.split(file, ',')[1]
    img_data = base64.urlsafe_b64decode(data_url + '=' * (4 - len(data_url) % 4))
    img_data = np.frombuffer(img_data, np.uint8)
    img_arr = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
    cv2.imwrite("./static/images/1.jpg", img_arr)
    return jsonify({'action': '成功'})


@app.route('/meibai/')
def meibais():
    meibai.face_whitening()
    return jsonify({'path': './static/images/meibai.jpg'})


@app.route('/quban/')
def qubans():
    quban.quban()
    return jsonify({'path': './static/images/quban.jpg'})


@app.route('/bao/')
def baos():
    bao.ColorEnhancement()
    return jsonify({'path': './static/images/bao.jpg'})


@app.route('/mopi/')
def mopis():
    quban.mopi()
    return jsonify({'path': './static/images/mopi.jpg'})


if __name__ == '__main__':
    app.run(port=5000)
    # 找到这个apps ,然后点击鼠标右键，找到run 然后点击
    # 最后点击出来的网址 http://127.0.0.1:5000
