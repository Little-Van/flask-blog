from flask import Flask, render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_script import Manager


app = Flask(__name__)
app.config['SECRET_KEY'] = '19920714'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0105@localhost/flasktest'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

moment = Moment(app)

manager = Manager(app)


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


db.drop_all()
db.create_all()

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
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('hello_world.html', form=form, name=session.get('name'), konwn=session.get('known', False))


@app.route('/login/<name>')
def user(name):
    return render_template('homepage.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()