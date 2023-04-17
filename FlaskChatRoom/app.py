from gevent import monkey

monkey.patch_all()

import os
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='gevent')


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     avatar_url = db.Column(db.String(120), nullable=False)


# db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    avatar_url = db.Column(db.String(120), nullable=False)


# with app.app_context():
#     db.create_all()


def get_random_avatar():
    avatars_dir = 'static/images/Head_picture'
    avatars = os.listdir(avatars_dir)
    avatar_file = random.choice(avatars)
    return os.path.join(avatars_dir, avatar_file)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        avatar_url = request.form['avatar_url']
        user = User(name=name, avatar_url=avatar_url)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index', user_id=user.id))
    avatars = [os.path.join('static/images/Head_picture', f) for f in os.listdir('static/images/Head_picture')]
    random.shuffle(avatars)
    return render_template('login.html', avatars=avatars)


@app.route('/')
def index():
    user_id = request.args.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if user is None:
        return redirect(url_for('login'))
    return render_template('index.html', user=user)


@socketio.on('send_message')
def handle_send_message(data):
    user_id = data['user_id']
    # user_name = data['user_name']  # 从数据中获取用户昵称
    # avatar_url = data['avatar_url']
    # message = data['message']
    user = User.query.get(user_id)
    # # 将用户昵称添加到广播的消息中
    # socketio.emit('receive_message',
    #               {'user_id': user_id, 'user_name': user_name, 'avatar_url': avatar_url, 'message': message})
    if user is not None:
        emit('receive_message', {'user_name': user.name, 'avatar_url': user.avatar_url, 'message': data['message']},
             broadcast=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=8000, websocket='gevent')
