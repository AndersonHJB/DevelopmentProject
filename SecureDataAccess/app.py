from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

password_data = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit_password', methods=['POST'])
def submit_password():
    password = request.form['password']
    valid_days = int(request.form['valid_days'])

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    expiration_date = datetime.now() + timedelta(days=valid_days)
    password_data[password_hash] = expiration_date

    flash(f"密码 '{password}' 已添加，有效期为 {valid_days} 天。")
    return redirect(url_for('index'))


@app.route('/validate_password', methods=['POST'])
def validate_password():
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if password_hash in password_data:
        expiration_date = password_data[password_hash]
        if datetime.now() <= expiration_date:
            return render_template('data.html')
        else:
            flash("密码已过期，请联系管理员获取新密码。")
            return redirect(url_for('index'))
    else:
        flash("密码错误，请检查后重新输入。")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
