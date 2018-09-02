import unittest
from app.models import User
from time import sleep


class UserNewModleCase(unittest.TestCase):

    def test_timeout_config(self):
        user = User(id=10)
        data = user.generate_confirmmation_token(2)
        sleep(3)
        user.confirm(data)
        self.assertFalse(user.confirmed or user.confirm(data))

    def test_error_config(self):
        user = User(id=10)
        data1 = user.generate_confirmmation_token(3600)
        data2 = b'wmt51j8HwIC5ZouTZjpxhhb9j-OHY'
        user.confirm(data2)
        self.assertFalse(user.confirmed or user.confirm(data2))

    def test_normal_config(self):
        user = User(id=10)
        data = user.generate_confirmmation_token(3600)
        user.confirm(data)
        self.assertTrue(user.confirmed or user.confirm(data))
