from flask import session, redirect, render_template, url_for, current_app
from datetime import datetime
from . import main
from .. import db
from ..models import User
from .forms import NameForm
from ..email import send_email
from ..models import Permission
from ..decorators import admin_required, permission_required
from flask_login import login_required
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
