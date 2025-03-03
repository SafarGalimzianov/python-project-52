from django.test import TestCase, Client
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.tasks.models import Task


class StatusModelTest(TestCase):
    def test_creation(self):
        name = 'Test Status'
        status = Status.objects.create(name=name)
        self.assertEqual(str(status), name)
        self.assertEqual(status.name, name)
    
    def test_uniqueness(self):
        name = 'Unique Status'
        Status.objects.create(name=name)
        with self.assertRaises(Exception):
            Status.objects.create(name=name)


class StatusViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
    def test_status_list(self):
        Status.objects.create(name='Test Status 1')
        Status.objects.create(name='Test Status 2')
        
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status 1')
        self.assertContains(response, 'Test Status 2')
        
    def test_status_create(self):
        status_data = {'name': 'New Test Status'}
        response = self.client.post(
            reverse('status_create'),
            status_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Status.objects.filter(name='New Test Status').exists())
        
    def test_status_update(self):
        status = Status.objects.create(name='Status To Update')
        response = self.client.post(
            reverse('status_update', kwargs={'pk': status.id}),
            {'name': 'Updated Status'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated Status')
        
    def test_status_delete(self):
        status = Status.objects.create(name='StatusToDelete')
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': status.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Status.objects.filter(name='StatusToDelete').exists())


class StatusDeleteWithRelationsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_delete_status_with_tasks(self):
        status = Status.objects.create(name='StatusWithTasks')

        Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=status,
            creator=self.user
        )

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': status.id}),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Status.objects.filter(name='StatusWithTasks').exists())
