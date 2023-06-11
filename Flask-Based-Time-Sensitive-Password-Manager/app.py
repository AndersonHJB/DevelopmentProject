from models import Admin, Password
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pickle

app = Flask(__name__)


def save_data(admins, passwords):
    with open('admins.pickle', 'wb') as f:
        pickle.dump(admins, f)
    with open('passwords.pickle', 'wb') as f:
        pickle.dump(passwords, f)


def load_data():
    try:
        with open('admins.pickle', 'rb') as f:
            admins = pickle.load(f)
    except FileNotFoundError:
        admins = []
    try:
        with open('passwords.pickle', 'rb') as f:
            passwords = pickle.load(f)
    except FileNotFoundError:
        passwords = []
    return admins, passwords


# 创建一个管理员账号
hashed_password = generate_password_hash("aiyuechuang")
admin = Admin("aiyuechuang", hashed_password)
admins, passwords = load_data()
admins.append(admin)
save_data(admins, passwords)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    admins, passwords = load_data()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for admin in admins:
            if admin.username == username and check_password_hash(admin.password, password):
                return redirect(url_for('manage_passwords'))
        return 'Invalid credentials'
    else:
        return render_template('admin.html')


@app.route('/manage-passwords', methods=['GET', 'POST'])
def manage_passwords():
    admins, passwords = load_data()
    if request.method == 'POST':
        password = request.form['password']
        valid_days = int(request.form['valid_days'])
        new_password = Password(password, datetime.utcnow(), valid_days)
        passwords.append(new_password)
        save_data(admins, passwords)
        return 'Password added'
    else:
        return render_template('manage_passwords.html', passwords=passwords)


@app.route('/content', methods=['GET', 'POST'])
def content():
    admins, passwords = load_data()
    if request.method == 'POST':
        password = request.form['password']
        for password_entry in passwords:
            if password_entry.password == password:
                if password_entry.valid_days == -1 or \
                        datetime.utcnow() - password_entry.created_at < timedelta(days=password_entry.valid_days):
                    # return 'Here is the content...'
                    return str(open("link.html", "r").read())
                else:
                    return 'Password expired'
        return 'Invalid password'
    else:
        return render_template('content.html')


def delete_expired_passwords():
    with open('passwords.pickle', 'rb') as f:
        passwords = pickle.load(f)

    for password in passwords:
        if password.valid_days != -1 and datetime.now() > password.created_at + timedelta(days=password.valid_days):
            passwords.remove(password)

    with open('passwords.pickle', 'wb') as f:
        pickle.dump(passwords, f)


scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_expired_passwords, trigger="interval", seconds=3600)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
