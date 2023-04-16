import os
import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from gevent import monkey
monkey.patch_all()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aiyuechuang'
socketio = SocketIO(app, async_mode='gevent')
# socketio = SocketIO(app)


def get_random_avatar():
    avatars_dir = 'static/images/Head_picture'
    avatars = os.listdir(avatars_dir)
    avatar_file = random.choice(avatars)
    # print(avatars)
    # print(avatar_file)
    return os.path.join(avatars_dir, avatar_file)


@app.route('/')
def index():
    avatar_url = get_random_avatar()
    return render_template('index.html', avatar_url=avatar_url)


@socketio.on('send_message')
def handle_send_message(data):
    emit('receive_message', data, broadcast=True)


if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', port=12345)
    socketio.run(app, host='0.0.0.0', port=8000)
    # socketio.run(app, host='localhost', port=12345)
    # socketio.run(app, host='192.168.31.155', port=12345)
