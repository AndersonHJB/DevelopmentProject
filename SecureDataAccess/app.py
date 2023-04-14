from flask import Flask, request, render_template, jsonify
from flask_frozen import Freezer
from markdown2 import Markdown
from passlib.hash import sha256_crypt
import json, time, sys
import os

app = Flask(__name__)
markdown = Markdown()
freezer = Freezer(app)

# 加载 json 数据
with open("users.json", "r") as f:
    users = json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]

        if user_name in users and sha256_crypt.verify(password, users[user_name]["password"]):
            # 验证有效期
            if "expiration" in users[user_name] and users[user_name]["expiration"] < time.time():
                return "访问权限已过期", 403

            with open(f"static/content/{user_name}.md", "r", encoding="utf-8") as content_file:
                content = content_file.read()

            html_content = markdown.convert(content)
            return render_template("content.html", content=html_content)

        return "无效的用户名或密码", 401

    return render_template("index.html")


if __name__ == "__main__":
    # app.run(debug=True)
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)
