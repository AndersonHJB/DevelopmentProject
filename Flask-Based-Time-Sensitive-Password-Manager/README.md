# Flask-Based Time-Sensitive Password Manager

## Initial intention of the project

为了解决，我在给学员、客户提供魔法🪄时，每个月都要维护更新节点。每个用户的有效期不同，每次都得查和计算，沉默成本很高，最后研发一个具有时效的密码访问系统。

## Technical Involvement

这个项目主要涉及以下技术和概念：

1. **Python**：Python 是一种流行的、易于学习的编程语言。在这个项目中，我们用 Python 来编写后端代码。

2. **Flask**：Flask 是一个用 Python 编写的轻量级 Web 应用框架。在这个项目中，我们用 Flask 来处理 HTTP 请求、渲染 HTML 模板、管理路由等。

3. **HTML**：HTML 是用来创建网页的标记语言。在这个项目中，我们用 HTML 来编写网页模板。

4. **Pickle**：Pickle 是 Python 的一个模块，可以把 Python 对象序列化为字节流，也可以从字节流中反序列化出 Python 对象。在这个项目中，我们用 Pickle 来保存和加载数据。

5. **密码哈希**：密码哈希是一种安全措施，用来防止密码在存储和传输过程中被窃取。在这个项目中，我们用 `werkzeug.security` 模块的 `generate_password_hash` 和 `check_password_hash` 函数来生成和检查密码哈希。

6. **HTTP方法**：HTTP 有多种方法，如 GET、POST、PUT、DELETE 等。在这个项目中，我们主要使用 GET 和 POST 方法。

7. **Web表单**：Web 表单是 HTML 的一部分，可以让用户输入数据并提交到服务器。在这个项目中，我们在 HTML 模板中创建了多个表单，用来实现登录、添加密码等功能。

8. **日期和时间操作**：在这个项目中，我们需要对日期和时间进行一些操作，如获取当前时间、计算时间差等。我们使用 Python 的 `datetime` 模块来完成这些操作。

9. **MVC模式**：MVC 是 Model-View-Controller 的缩写，是一种常见的软件设计模式。在这个项目中，我们的数据模型（Model）是 `Admin` 和 `Password` 类，视图（View）是 HTML 模板，控制器（Controller）是视图函数。

## Future

- [ ] 功能性
    - [x] 密码时效性
    - [x] 密码后台添加
    - [x] 密码设置时效「-1为永久有效」
    - [ ] 时效密码删除
        - [ ] 自动删除
        - [ ] 手动删除
    - [ ] 
- [ ] 后台管理
- [ ] UI
    - [x] 草图界面
    - [ ] 
