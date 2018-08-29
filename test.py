from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql


# 创建flask对象
app = Flask(__name__)

# 配置flask配置对象中键：SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:0105@localhost/test"

# 配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动

app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# 获取SQLAlchemy实例对象，接下来就可以使用对象调用数据
db = SQLAlchemy(app)


# 创建模型对象`
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# 1.创建表


db.drop_all()


db.create_all()


# 2.增加记录
admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')
db.session.add(admin)
db.session.add(guest)
db.session.commit()

'''
# 3.查询记录,注意查询返回对象，如果查询不到返回None
User.query.all()  # 查询所有
User.query.filter_by(username='admin').first()   # 条件查询
User.query.order_by(User.username).all()  # 排序查询
User.query.limit(1).all()   # 查询1条
User.query.get(id = 123)  # 精确查询

# 4.删除
user = User.query.get(id = 123)
db.session.delete(user)
db.session.commit()
'''