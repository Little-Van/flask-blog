import unittest
from app.models import User
from app.auth.forms import LoginForm


class UserLoginTestCase(unittest.TestCase):

    def test_email_adress_notvalid(self):
        guest = LoginForm(email='123456')
        self.assertTrue(guest.email.data)

    def test_email_notvalid(self):
        guest = LoginForm(email='little_yang@126.com', password='123')
        user = User.query.filter_by(email=guest.email.data).first()
        self.assertTrue(user.verify_password(guest.password.data) is not True)

    def test_email_notvalid(self):
        guest = LoginForm(email='little_yang@126.com', password='yang')
        user = User.query.filter_by(email=guest.email.data).first()
        self.assertTrue(user.verify_password(guest.password.data) is True)
