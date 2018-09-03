from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=([DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.*$]', 0,
                           "Username must have only letters,numbers,dots or underscores")]))
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message=
                                                                             'Password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')

    def validate_username(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('Username already registered!')


class ResetPasswordRequest(FlaskForm):
    email = StringField('Enter email you register', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('look back password')


class ResetPassword(FlaskForm):
    password = PasswordField('New password', validators=[DataRequired(), EqualTo('password2', message=
                                                                            'Password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset')


class ChangeEmailRequest(FlaskForm):
    email = StringField('New email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Change Email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')


class ChangePassword(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired(), EqualTo('password2', message=
                                                                            'Password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset')
