from flask import Flask, render_template
from flask_script import Manager

app = Flask(__name__)

manager = Manager(app)


@app.route('/')
def index():
    return render_template('hello_world.html')


@app.route('/login')
def user():
    return render_template('homepage.html')


if __name__ == '__main__':
    manager.run()