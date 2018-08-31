import os
import pymysql


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '38567210'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUNJECT_PREFIX = '[Flasky]'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + os.environ.get('DEV_DATABASE_URL') + '/flasktest'


class TestingConfig(Config):
    TESTING = True
    QLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + os.environ.get('DEV_DATABASE_URL') + '/flasktest'


class ProductionConfig(Config):
    QLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + os.environ.get('DEV_DATABASE_URL') + '/flasktest'


config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }

