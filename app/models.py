from . import db
from werkzeug.security import generate_password_hash, check_password_hash


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
    password_hash = db.Column(db.String(128))
    pro_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    @property
    def password(self):
        raise AttributeError('password os not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)
