from rest_framework.test import APITestCase
from authentication.models import User

class TestModel(APITestCase):
    
    def test_creates_user(self):
        user=User.objects.create_user('job','j@gmail.com','pass1234')
        self.assertIsInstance(user,User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email,'j@gmail.com')
        