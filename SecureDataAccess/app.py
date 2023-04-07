from flask import Flask, render_template, request, redirect, url_for, flash
import json
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"


# 从JSON文件中加载数据
def load_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data


# 保存数据到JSON文件
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)


# 验证密码
def is_password_valid(password):
    data = load_data()
    if password in data.keys():
        expiration_date = datetime.datetime.strptime(data[password]["expiration"], "%Y-%m-%d")
        if datetime.datetime.now() <= expiration_date:
            return True
    return False


# 首页
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form["password"]
        if is_password_valid(password):
            content = load_data()[password]["content"]
            return render_template("content.html", content=content)
        else:
            flash("密码错误或已过期。")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
