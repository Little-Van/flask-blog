from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('hello_world.html')


@app.route('/login/<name>')
def user(name):
    return render_template('homepage.html', name=name)

