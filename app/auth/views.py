from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User
from flask_login import login_user, logout_user, login_required
import sqlalchemy
from .. import db


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    form = LoginForm(email='chenpanpan@qq.com', password='123456')
    print(form.validate())
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
        except sqlalchemy.exc.ProgrammingError:
            user = None
        finally:
            if user and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.hello'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if test.validate_on_submit():
        new_user = User(user_name=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('main.hello'))
    return render_template('auth/register.html', form=form)

