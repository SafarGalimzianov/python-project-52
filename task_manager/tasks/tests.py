from django.test import TestCase, Client
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User


class TaskModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name='Test Status')
        self.creator = User.objects.create_user(
            username='creator',
            password='creatorpass123'
        )
        self.executor = User.objects.create_user(
            username='executor',
            password='executorpass123'
        )
        self.label1 = Label.objects.create(name='Test Label 1')
        self.label2 = Label.objects.create(name='Test Label 2')

    def test_creation(self):
        name = 'Test Task'
        description = 'Test Description'
        task = Task.objects.create(
            name=name,
            description=description,
            status=self.status,
            creator=self.creator,
            executor=self.executor
        )
        task.labels.add(self.label1, self.label2)

        self.assertEqual(task.description, str(task))
        self.assertEqual(task.name, name)
        self.assertEqual(task.description, description)
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.creator, self.creator)
        self.assertEqual(task.executor, self.executor)

        self.assertEqual(list(task.labels.all()), [self.label1, self.label2])


class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

        self.status = Status.objects.create(name='Test Status')
        self.label = Label.objects.create(name='Test Label')

    def test_task_list(self):
        task1 = Task.objects.create(
            name='Test Task 1',
            description='Description 1',
            status=self.status,
            creator=self.user
        )
        task2 = Task.objects.create(
            name='Test Task 2',
            description='Description 2',
            status=self.status,
            creator=self.user
        )

        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Test Task 2')

    def test_task_create(self):
        task_data = {
            'name': 'New Test Task',
            'description': 'New Description',
            'status': self.status.id,
            'labels': [self.label.id],
            'executor': self.user.id
        }

        response = self.client.post(
            reverse('task_create'),
            task_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        created_task = Task.objects.filter(name='New Test Task').first()
        self.assertIsNotNone(created_task)
        self.assertEqual(created_task.description, 'New Description')
        self.assertEqual(created_task.status, self.status)
        self.assertEqual(str(created_task.creator), self.user.username)
        self.assertEqual(str(created_task.executor), self.user)
        self.assertEqual(list(created_task.labels.all()), [self.label])

    def test_task_detail(self):
        task = Task.objects.create(
            name='Task To View',
            description='View Description',
            status=self.status,
            creator=self.user
        )

        response = self.client.get(
            reverse('task_show', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task To View')
        self.assertContains(response, 'View Description')

    def test_task_update(self):
        task = Task.objects.create(
            name='Task To Update',
            description='Update Description',
            status=self.status,
            creator=self.user
        )

        updated_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.user.id
        }

        response = self.client.post(
            reverse('task_update', kwargs={'pk': task.id}),
            updated_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task')
        self.assertEqual(task.description, 'Updated Description')

    def test_task_delete(self):
        task = Task.objects.create(
            name='Task To Delete',
            description='Delete Description',
            status=self.status,
            creator=self.user
        )

        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(name='Task To Delete').exists())


class TaskDeletePermissionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='user1pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='user2pass123'
        )
        self.status = Status.objects.create(name='Test Status')

    def test_user_can_only_delete_own_task(self):
        task = Task.objects.create(
            name='User1 Task',
            description='Task created by user1',
            status=self.status,
            creator=self.user1
        )

        self.client.login(username='user2', password='user2pass123')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.id}),
            follow=True
        )

        self.assertTrue(Task.objects.filter(name='User1 Task').exists())

        self.client.login(username='user1', password='user1pass123')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.id}),
            follow=True
        )

        self.assertFalse(Task.objects.filter(name='User1 Task').exists())


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='user1pass123',
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='user2pass123',
        )

        self.status1 = Status.objects.create(name='Status 1')
        self.status2 = Status.objects.create(name='Status 2')

        self.label1 = Label.objects.create(name='Label 1')
        self.label2 = Label.objects.create(name='Label 2')

        self.task1 = Task.objects.create(
            name='Task 1',
            description='Description 1',
            status=self.status1,
            creator=self.user1,
            executor=self.user1
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Task 2',
            description='Description 2',
            status=self.status2,
            creator=self.user2,
            executor=self.user2
        )
        self.task2.labels.add(self.label2)

        self.task3 = Task.objects.create(
            name='Task 3',
            description='Description 3',
            status=self.status1,
            creator=self.user1,
            executor=self.user2
        )
        self.task3.labels.add(self.label1, self.label2)

        self.client = Client()
        self.client.login(username='user1', password='user1pass123')

    def test_filter_by_status(self):
        response = self.client.get(f"{reverse('tasks')}?status={self.status1.id}")
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_executor(self):
        response = self.client.get(f"{reverse('tasks')}?executor={self.user2.id}")
        self.assertContains(response, 'Task 2')
        self.assertContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 1')

    def test_filter_by_label(self):
        response = self.client.get(f"{reverse('tasks')}?labels={self.label1.id}")
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 2')

    def test_filter_self_tasks(self):
        response = self.client.get(f"{reverse('tasks')}?self_tasks=1")
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 2')
