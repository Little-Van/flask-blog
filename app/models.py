from . import db


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
