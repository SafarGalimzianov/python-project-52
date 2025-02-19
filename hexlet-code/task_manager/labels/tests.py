from django.test import TestCase
from task_manager.labels.models import Label

# Create your tests here.

class LabelModelTest(TestCase):
    def test_field(self):
        field_content = 'label field'
        label_object = Label.objects.create(label=field_content)
        self.assertEqual(field_content, str(label_object))
