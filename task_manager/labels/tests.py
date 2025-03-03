from django.test import TestCase, Client
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class LabelModelTest(TestCase):
    def test_creation(self):
        name = 'Test Label'
        label = Label.objects.create(name=name)
        self.assertEqual(str(label), name)
        self.assertEqual(label.name, name)
    
    def test_uniqueness(self):
        name = 'Unique Label'
        Label.objects.create(name=name)
        with self.assertRaises(Exception):
            Label.objects.create(name=name)


class LabelViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
    def test_label_list(self):
        Label.objects.create(name='Test Label 1')
        Label.objects.create(name='Test Label 2')
        
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label 1')
        self.assertContains(response, 'Test Label 2')
        
    def test_label_create(self):
        label_data = {'name': 'New Test Label'}
        response = self.client.post(
            reverse('label_create'),
            label_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(name='New Test Label').exists())
        
    def test_label_update(self):
        label = Label.objects.create(name='Label To Update')
        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.id}),
            {'name': 'Updated Label'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        label.refresh_from_db()
        self.assertEqual(label.name, 'Updated Label')
        
    def test_label_delete(self):
        label = Label.objects.create(name='Label To Delete')
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter(name='Label To Delete').exists())


class LabelDeleteWithRelationsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
    def test_delete_label_with_tasks(self):
        label = Label.objects.create(name='Label With Tasks')
        
        status = Status.objects.create(name='Test Status')
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=status,
            creator=self.user
        )
        task.labels.add(label)
        
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.id}),
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(name='Label With Tasks').exists())
