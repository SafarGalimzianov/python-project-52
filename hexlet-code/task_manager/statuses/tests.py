from django.test import TestCase
from task_manager.statuses.models import Status

# Create your tests here.

class StatusModelTest(TestCase):
    def test_field(self):
        field_content = 'status field'
        label_object = Status.objects.create(status=field_content)
        self.assertEqual(field_content, str(label_object))
