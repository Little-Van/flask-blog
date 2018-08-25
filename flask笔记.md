# flask学习笔记
## 路由和视图函数
  - 客户端把请求发给web服务器，Web服务器再把请求发给flask程序实例。程序实例将URL与执行功能的函数一一对应，从而完成前端请求->后端处理->前端显示结果这个过程。处理URL和函数之间映射关系的程序称之为路由。
  - URL：统一资源定位符，互联网协议标准之一，完整的描述格式为协议://用户名:密码@子域名.域名.顶级域名:端口号/目录/文件名.文件后缀?参数=值#标志
  - flask中使用程序实例提供的app.route作为装饰器，把装饰的函数注册为路由。
### 装饰器app.route
- app.route(url, methods, endpoint, defaults):
  - url:为前端请求地址
  - methods：允许前端请求的方式，如POST，GET等，get请求参数包含在URL中，POST请求参数包含 在request对象中，GET产生一次TCP数据包，post产生两次TCP数据包；
  - endpoint：url的反向地址，可以通过url_for还原
  - defaults:视图函数默认参数，例defaults={‘name’=‘cuper’}
### 装饰器app.errorhandler(error_num)
- 自定义错误页面的返回
### app.config
- app.config中保存了程序实例的配置，可以通过字典的方式来进行访问，常用的如下：
  - static_folder = 'static',  # 静态文件目录的路径 默认当前项目中的static目录
  - static_url_path = None,  # 静态文件目录的url路径 默认不写是与static_folder同名,远程静态文件时复用
  - template_folder = 'templates'  # template模板目录, 默认当前项目中的templates目录
## flask常用模块以及函数
###  redirect（url）
- 生成重定向响应
- 将参数中的url传递给前端，前端发起新的响应，交给对应的路由进行处理
### render_template（‘×.html’,key=value,...）
- 默认返回template文件下渲染的模板
- 传递关键字参数，变量可以是值、列表、字典，可以传递多个关键字参数，所以可以引用关键字分配，即使用两个‘\*'来进行字典关键字的分配，例如 **{'a':name, 'b':age}  -> a=name, b=age
### request
- request为请求上下文，request对象中封装了http的所有请求对象
- request.mothod:
  - 储存前端的请求方式，与路由进行匹配
- request.form:
  - 获取form表单中的数据，以类似字典的形式，数据储存在一个ImmutableMultiDict
对象中，可以使用字典的各种方法进行访问
- request.args:
  - 获取URL中传递的参数，以类似字典的形式，数据储存在一个ImmutableMultiDict对象中，可以使用字典的各个方法进行访问，与form不同的两个参数传递前端中不同位置的参数
- request.values:
  - 获取前端中所有的参数，并将数据储存在ImmutableMultiDict对象中，使用to_dict可以将其转化为一个字典，如果url和form中的Key重名的话,form中的同名的key中value会被url中的value覆盖
- request.cookies:
    - 将浏览器中的cookie一并传入
- request.headers:
  - 封装前端的各个信息，采用字典形式返回各个对象的信息
- request.files:
  - 传递前端传入的文件对象，储存在ImmutableMultiDict中，可以使用字典的访问方法，通过关键字file进行访问，调用file的方法save可以将文件保存指定目录，默认为当前目录
### session
- Flask中使用session请求上下文储存临时变量，因为reques对象中的变量在重定向之后内容会全部丢失，所以如果我们需要保存特定的数据，可以使用session来进行储存
- session的使用：
  - session使用之前需要在指定secret_key,需要修改app实例中的secret_key,来对内容进行加密处理
  - session使用字典来保存数据，可直接使用中字典的方法
### current_app
- 当前flask激活的app实例，需要激活之后才能够使用，属于程序上下文
### g
- 程序上下文，处理请求时用作临时存储的对象，每次请求都会重设这个变量
## flask的模板Jinja2
1. 访问render_template传递的变量：
    - 在html内部使用{{name}}表示，name即为外界传入的变量；
2. 使用for循环结构：
    - 语法结构:
```Jinja2
    {%    for  x  in  y      %}
         {{x}}
    {%    endfor   %}
```
3. 使用if--esif-else结构：
```
    {%  if condition1 %}
    {%  elif condition2 %}
    {%  else  %}
    {%  endif %}
```
4. Jinja2中的函数可以直接作为参数由后端传递，使用方法与python也是一致的
5. Jinja2模板复用block
    - 声明一个基类的模板，在模板中定义block，例如：base.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Welcome OldboyEDU</h1>
    <h2>下面的内容是不一样的</h2>
    {% block content %}                #指明block模块的位置

    {% endblock %}
    <h2>上面的内容是不一样的,但是下面的内容是一样的</h2>
    <h1>OldboyEDU is Good</h1>
</body>
</html>
```
  - 在该模板基础上进行继承，并添加：info.html
```
{% extends "index.html" %}  #继承模板base.html
{% block content %}         #拓展black的内容
    <form>
        用户名:<input type="text" name="user">
        密码:<input type="text" name="pwd">
    </form>
{% endblock %}
```
  - 使用该功能可以快速进行拓展开发
6. Jinja2的导入模块 include
    - 模块：login.html
```html
<form>
    用户名:<input type="text" name="user">
    密码:<input type="text" name="pwd">
</form>
```
  - 模块：info.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Welcome OldboyEDU</h1>
    <h2>下面的内容是不一样的</h2>
    {% include "login.html" %}   #导入模块
    <h2>上面的内容是不一样的,但是下面的内容是一样的</h2>
    <h1>OldboyEDU is Good</h1>
</body>
</html>
```
