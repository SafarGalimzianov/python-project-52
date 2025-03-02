from django.test import TestCase
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class TaskModelTest(TestCase):
    def test_field(self):
        field_content = {
            'status': Status.objects.create(status='status field'),
            'labels': [
                Label.objects.create(label='label field 1'),
                Label.objects.create(label='label field 2')
            ],
            'creator': User.objects.create_user(
                username='creator username field',
                password='creator password field'
            ),
            'responsible': User.objects.create_user(
                username='responsible username field',
                password='responsible password field'
            ),
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
        task_object.labels.set([field_content['labels'][0]])
        self.assertEqual(field_content['labels'][0],
                         list(task_object.labels.all())[0])
        task_object.labels.add(field_content['labels'][1])
        self.assertEqual(field_content['labels'][1],
                         list(task_object.labels.all())[1])
        self.assertEqual(field_content['labels'],
                         list(task_object.labels.all()))
