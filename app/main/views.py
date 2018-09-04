from flask import redirect, render_template, url_for, current_app, abort, flash
from datetime import datetime
from . import main
from .. import db
from ..models import User, Post, Permission
from .forms import PostForm, EditProfileForm, EditProfileAdminForm
from ..decorators import admin_required, permission_required
from flask_login import login_required, current_user


@main.route('/', methods=['POST', 'GET'])
def index():
    form = PostForm()
    if form.validate_on_submit() and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body=form.body.data, author=current_user._get_current_object())
        return redirect(url_for('main.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)


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



