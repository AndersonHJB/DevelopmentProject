from flask import Flask, render_template, request, redirect, url_for
import datetime
import hashlib

app = Flask(__name__)

# 存储密码和对应的有效期
# password_data = {"aiyc": "100"}
password_data = {
    "4a4c378d47827e8dc646c6112d0fd807fd6f1e21f42af831e9fd9d0d96b2f71a": datetime.datetime.now() + datetime.timedelta(days=7)
}



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit_password', methods=['POST'])
def submit_password():
    password = request.form['password']
    valid_days = int(request.form['valid_days'])

    # 用哈希值作为密码的唯一标识
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # 设置密码有效期
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=valid_days)
    password_data[password_hash] = expiration_date

    return redirect(url_for('index'))


@app.route('/validate_password', methods=['POST'])
def validate_password():
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if password_hash in password_data:
        expiration_date = password_data[password_hash]
        if datetime.datetime.now() <= expiration_date:
            return render_template('data.html')
        else:
            return "密码已过期，请联系管理员获取新密码。", 403
    else:
        return "密码错误，请检查后重新输入。", 403


if __name__ == '__main__':
    app.run(debug=True)
