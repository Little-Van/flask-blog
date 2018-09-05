from flask import Flask, render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
import os
from threading import Thread


app = Flask(__name__)
app.config['SECRET_KEY'] = '19920714'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0105@localhost/flasktest'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASK_ADMIN'] = os.environ.get('FLASK_ADMIN')
app.config['FLASKY_MAIL_SUNJECT_PREFIX'] = '[Flasky]'


db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

moment = Moment(app)

manager = Manager(app)

mail = Mail(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='hobby', lazy='dynamic')

    def __repr__(self):
        return '<Product {}>'.format(self.pro_name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True)
    pro_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return '<User {}>'.format(self.user_name)


'''
pro_banana = Product(pro_name='banana')
pro_apple = Product(pro_name='apple')
pro_orange = Product(pro_name='orange')
user_little = User(user_name='little', hobby=pro_banana)
user_runlan = User(user_name='runlan', hobby=pro_apple)
user_cuper = User(user_name='cuper', hobby=pro_banana)
user_lisa = User(user_name='jinjia', hobby=pro_orange)


db.session.add_all([pro_banana, pro_apple, pro_orange, user_little, user_runlan, user_cuper, user_lisa])
db.session.commit()
'''


def send_thr_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, tempalte,  **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUNJECT_PREFIX'] + subject, sender=app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(tempalte + '.txt', **kwargs)
    msg.html = render_template(tempalte + '.html', **kwargs)
    thr_mail = Thread(target=send_thr_mail, args=(app, msg))
    thr_mail.start()
    return thr_mail


def make_shell_context():
    return dict(app=app, db=db, User=User, Product=Product)


manager.add_command('shell', Shell(make_context=make_shell_context))


@app.route('/', methods=['POST', 'GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.name.data).first()
        if not user:
            user = User(user_name=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASK_ADMIN']:
                send_email(app.config['FLASK_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), konwn=session.get('known', False))


@app.route('/login/<name>')
def user(name):
    return render_template('_post.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
