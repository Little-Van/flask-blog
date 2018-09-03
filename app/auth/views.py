from flask import render_template, redirect, request, url_for, flash, current_app
from . import auth
from .forms import LoginForm, RegisterForm, ResetPasswordRequest, ResetPassword, ChangeEmailRequest, ChangePassword
from ..models import User
from ..email import send_email
from flask_login import login_user, logout_user, login_required, current_user
import sqlalchemy
from .. import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
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
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(user_name=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirmmation_token()
        send_email(new_user.email, 'Confirm Your Account', 'auth/email/confirm', user=new_user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(request.args.get('next') or url_for('main.hello'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account.Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def befor_request():
    if current_user.is_authenticated and not current_user.confirmed \
                                        and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect((url_for('main.index')))
    return render_template('auth/unconfirmed.html', user=current_user)


@auth.route('/resetpasswordrequest', methods=['POST', 'GET'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user. generate_reset_token()
            send_email(form.email.data, 'Password reset', 'auth/email/resetpasswordrequest', token=token, form=form)
            flash('A reset confirmmation has been sent to you by email')
            return redirect(url_for('auth.login'))
        else:
            flash('The email is invalid,please confirm and enter again!')
            return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/resetpasswdrequest.html', form=form)


@auth.route('/resetpassword/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        use_data = User.query.get(data.get('reset')).id
    except:
        flash('Invalid information,please confirmed')
        return redirect(url_for('auth.reset_password_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        if User.password_reset(token, form.password.data):
            flash('You has reset your password successfully')
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/resetpassword.html', form=form)


@auth.route('/change_email_request', methods=['POST', 'GET'])
@login_required
def change_email_request():
    form = ChangeEmailRequest()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            token = current_user.generate_email_change_token(form.email.data)
            send_email('form.email.data', 'Confirm your account', 'auth/email/change_email_request', form=form, token=token)
            flash('A confirmmation has been sent to you by the new email account!')
        else:
            flash('Invalid email or password!')
        return redirect(url_for('auth.change_email_request'))
    return render_template('auth/changeemailrequest.html', form=form)


@auth.route('/change_email/<token>', methods=['POST', 'GET'])
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email has been updated!')
        return redirect(url_for('auth.logout'))
    else:
        flash('Invalid information')
        return redirect(url_for('auth.change_email_request'))


@auth.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('You have change your password successfully!')
            return redirect(url_for('auth.logout'))
        else:
            flash('In valid password,please confirm!')
            return redirect(url_for('auth.change_password'))
    return render_template('auth/changepassword.html', form=form)


