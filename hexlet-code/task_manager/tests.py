from django.test import TestCase
from task_manager.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User

# Create your tests here.

class LabelModelTest(TestCase):
    def test_field(self):
        field_content = {
            'status': Status.objects.create(status='status field'),
            'labels': [Label.objects.create(label='label field 1'), Label.objects.create(label='label field 2')],
            'creator': User.objects.create_user(username='creator username field', password='creator password field'),
            'responsible': User.objects.create_user(username='responsible username field', password='responsible password field'),
            'description': 'description field',
        }
        task_object = Task.objects.create(
            status=field_content['status'],
            creator=field_content['creator'],
            responsible=field_content['responsible'],
            description=field_content['description'],
        )
        self.assertEqual(field_content['description'], str(task_object))
        self.assertEqual(field_content['status'], task_object.status)
        task_object.labels.set(field_content['labels'][0])
        self.assertEqual(field_content['labels'][0], task_object.labels.all()[0])
        task_object.labels.add(field_content['labels'][1])
        self.assertEqual(field_content['labels'][1], task_object.labels.all()[1])
        self.assertEqual(field_content['labels'], list(task_object.labels.all()))


'''
from django.test import TestCase
from task_manager.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskModelTests(TestCase):
    def setUp(self):
        self.status = Status.objects.create(status="Done")
        self.label = Label.objects.create(label="Low Priority")
        self.user = User.objects.create_user(username="task_creator", password="secret")

    def test_create_task(self):
        task = Task.objects.create(
            status=self.status,
            creator=self.user,
            responsible=self.user,
            description="Test task description"
        )
        task.labels.add(self.label)
        self.assertEqual(str(task), "Test task description")
        self.assertEqual(task.status, self.status)
        self.assertIn(self.label, task.labels.all())
'''