from django.test import TestCase
from task_manager.users.models import User


class UserModelTest(TestCase):
    def test_field(self):
        field_content = {
            'username': 'username field',
            'password': 'password field',
        }
        label_object = User.objects.create(
            username=field_content['username'],
            password=field_content['password']
        )
        self.assertEqual(field_content['username'], str(label_object))
