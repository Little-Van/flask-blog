from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)
app.config["DEBUG"] = True
print(app.config['ENV'])


@app.route('/user/<name>')
def hello_user(name):
    return render_template('user.html', name=name)


@app.route('/')
def hello_world():
    print('hello,world!')
    return render_template('user.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


'''
@app.route('/req', methods=['POST', 'GET'])
def wow_test():
    print(request.files)
    print(request.files['file'])
    my_file = request.files['file']
    my_file.save('littleBoy.txt')
    return 'OK,little boy!'
'''


# 访问地址 : /info 浏览器跳转至 /infos
@app.route("/info", strict_slashes=True, redirect_to="/infos")
def student_info():
    return "Hello Old boy info"


@app.route("/infos", strict_slashes=False)
def student_infos():
    return "Hello Old boy ru"


if __name__ == '__main()__':

    app.run()