from django.db import models

from django.test import TestCase

class UserTest(TestCase):
    def test_new_user(self):
        with self.assertRaises(ValueError):
            return '%s'% 'User'
