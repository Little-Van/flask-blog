from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment

app = Flask(__name__)

bootstrap = Bootstrap(app)

moment = Moment(app)


@app.route('/')
def index():
    return render_template('hello_world.html', current_time=datetime.utcnow())


@app.route('/login/<name>')
def user(name):
    return render_template('homepage.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

