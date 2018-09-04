from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, ValidationError
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Read name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=([DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.*$]', 0,
                           "Username must have only letters,numbers,dots or underscores")]))
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.role_name) for role in Role.query.order_by(Role.role_name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != User.query.filter_by(email=field.data).first()\
                and field.data != self.user.email:
            raise ValidationError('Email already registered!')

    def validate_username(self, field):
        if field.data != User.query.filter_by(user_name=field.data).first() \
                and field.data != self.user.user_name:
            raise ValidationError('Username already in use!')


class PostForm(FlaskForm):
    body = TextAreaField("what's your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


