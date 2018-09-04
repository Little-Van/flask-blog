from flask import session, redirect, render_template, url_for, current_app, abort, flash
from datetime import datetime
from . import main
from .. import db
from ..models import User
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from ..email import send_email
from ..models import Permission
from ..decorators import admin_required, permission_required
from flask_login import login_required, current_user
import pymysql
import sqlalchemy


@main.route('/', methods=['POST', 'GET'])
def index():
    form = NameForm()
    guest = None
    if form.validate_on_submit():
        try:
            guest = User.query.filter_by(user_name=form.name.data).first()
        except sqlalchemy.exc.ProgrammingError:  # 捕获数据库表不存在异常并创建列表，使用exception as e，e是一个对象，e.__class__为异常所属类
            db.create_all()
        finally:
            if not guest:
                user_model = User(user_name=form.name.data)
                db.session.add(user_model)
                db.session.commit()
                session['known'] = False
                if current_app.config['FLASK_ADMIN']:
                    send_email(current_app.config['FLASK_ADMIN'], 'New User', 'mail/new_user', user=user_model)
            else:
                session['known'] = True
            session['name'] = form.name.data
            form.name.data = ''
            return redirect(url_for('main.index'))
    return render_template('hello_world.html', form=form, name=session.get('name'), konwn=session.get('known', False),
                           current_time=datetime.utcnow())


@main.route('/login/success')
def hello():
    return render_template('homepage.html')


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return render_template('homepage.html')


@main.route('/moderators')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return render_template('homepage.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(user_name=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated successfully!')
        return redirect(url_for('main.user', username=current_user.user_name))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.user_name = form.username.data
        user.confirmed = form.confirmed.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        if not user.is_administrator():
            user.role = User.query.get(form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated!')
        return redirect(url_for('main.user', username=user.user_name))
    form.email.data = user.email
    form.username.data = user.user_name
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form)
