import unittest
from app.models import User
from app.auth.forms import LoginForm


class UserLoginTestCase(unittest.TestCase):

    def test_normal_login(self):
        user = User.query.filter_by(user_name='little').first()
        print(user)
        self.assertTrue(user is not None)

    def test_email_notvalid(self):
        guest = LoginForm(email='little_van@126.com', password='123')
        user = User.query.filter_by(email=guest.email.data).first()
        self.assertTrue(user.verify_password(guest.password.data) is not True)


