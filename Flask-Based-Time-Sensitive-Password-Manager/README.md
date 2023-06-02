# Flask-Based Time-Sensitive Password Manager: 教学文档

本教学文档将引导您如何使用Python的Flask框架，构建一个具有时效性密码管理功能的Web应用程序。

## 一、项目概述

在这个项目中，我们将创建一个简单的Web应用，管理员可以在后台管理界面添加有时效性的密码。当密码过期，用户就不能用这个密码查看受保护的内容了。管理员也可以创建永不过期的密码。用户可以通过输入正确的密码来查看受保护的内容。

## 二、开发环境配置

首先，我们需要设置开发环境。确保你已经安装了Python和pip，然后使用pip安装Flask：

```bash
pip install flask
```

此外，我们还需要安装werkzeug，用于生成和检查密码哈希：

```bash
pip install Werkzeug
```

## 三、项目结构

首先，我们来创建项目的文件结构。项目的根目录下有两个Python文件（app.py 和 models.py），一个templates文件夹用来存放HTML模板，还有两个pickle文件（admins.pickle 和 passwords.pickle）用来存储管理员和密码数据：

```
/
├── app.py
├── models.py
├── templates/
│   ├── index.html
│   ├── admin.html
│   ├── manage_passwords.html
│   └── content.html
├── admins.pickle
└── passwords.pickle
```

接下来，我们来详细看看每个文件和文件夹的内容。

## 四、编写代码

### 1. 数据模型（models.py）

首先，我们创建数据模型。这里我们需要两个类：Admin 和 Password。Admin 类用来存储管理员的用户名和密码（哈希值），Password 类用来存储密码、创建时间和有效期。

```python
from datetime import datetime

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Password:
    def __init__(self, password, created_at, valid_days):
        self.password = password
        self.created_at = created_at
        self.valid_days = valid_days
```

### 2. 应用主体（app.py）

然后，我们创建Flask应用的主体，并定义路由和视图函数。

首先，我们需要导入需要的模块，并创建Flask应用：

```python
from flask import Flask, request, render_template, redirect, url_for
from models import Admin, Password
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import pickle

app = Flask(__name__)
```

然后，我们定义两个辅助函数来保存和加载数据：

```python
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
        with open('

passwords.pickle', 'rb') as f:
            passwords = pickle.load(f)
    except FileNotFoundError:
        passwords = []
    return admins, passwords
```

接下来，我们创建一个管理员账户，管理员的用户名和密码被硬编码为"admin"和"password"。在真实的应用场景中，应该提供用户注册和修改密码的功能：

```python
hashed_password = generate_password_hash("password")
admin = Admin("admin", hashed_password)
admins, passwords = load_data()
admins.append(admin)
save_data(admins, passwords)
```

然后，我们定义了四个路由和视图函数：首页、管理员登录页面、密码管理页面和内容页面：

```python
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
                    return 'Here is the content...'
                else:
                    return 'Password expired'
        return 'Invalid password'
    else:
        return render_template('content.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. HTML模板（templates）

在`templates`文件夹中，我们需要四个HTML模板：首页、管理员登录页面、密码管理页面和内容页面。

这里给出一个基础的模板例子。你可以根据需要增加更多的HTML元素和CSS样式。

* `index.html`：

```html
<!DOCTYPE html>
<html>
<head>
    <title>首页</title>
</head>
<body>
    <h1>Welcome to our website!</h1>
    <a href="/admin">Admin Login</a>
    <a href="/content">View Content</a>
</body>
</html>
```

* `admin.html`：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
</head>
<body>
    <h1>Admin Login</h1>
    <form method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <input type="submit" value="Login">
   

 </form>
</body>
</html>
```

* `manage_passwords.html`：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Manage Passwords</title>
</head>
<body>
    <h1>Manage Passwords</h1>
    <form method="post">
        <label for="password">Password:</label>
        <input type="text" id="password" name="password" required>
        <label for="valid_days">Valid Days (-1 for never expire):</label>
        <input type="number" id="valid_days" name="valid_days" required>
        <input type="submit" value="Add Password">
    </form>
    <h2>Existing Passwords:</h2>
    <ul>
        {% for password in passwords %}
        <li>{{ password.password }} (Created at: {{ password.created_at }}, Valid days: {{ password.valid_days }})</li>
        {% endfor %}
    </ul>
</body>
</html>
```

* `content.html`：

```html
<!DOCTYPE html>
<html>
<head>
    <title>View Content</title>
</head>
<body>
    <h1>Enter Password to View Content</h1>
    <form method="post">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
```

到此为止，基于Flask的时效性密码管理系统就已经创建完成了！你可以运行`app.py`文件来启动这个应用，然后在浏览器中访问`http://localhost:5000/`查看效果。

以上只是一个基础的项目，实际的应用可能需要更多的功能和安全措施，例如用户注册和密码修改、密码哈希和加盐、HTTPS等。