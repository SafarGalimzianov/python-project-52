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
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Test Label')
        
    def test_label_list(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label')
        
    def test_label_create(self):
        response = self.client.post(
            reverse('label_create'),
            {'name': 'New Label'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter\
                        (name='New Label').exists())
        
    def test_label_update(self):
        response = self.client.post(
            reverse('label_update', kwargs={'pk': self.label.id}),
            {'name': 'Updated Label'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')
        
    def test_label_delete(self):
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': self.label.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter\
                         (id=self.label.id).exists())


class LabelDeleteWithRelationsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.label = Label.objects.create(name='Related Label')
        self.status = Status.objects.create(name='Test Status')

        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            creator=self.user
        )
        self.task.labels.add(self.label)
        
    def test_delete_label_with_tasks(self):
        """Test that a label cannot be deleted if it's used in tasks"""
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': self.label.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        self.assertIn('error', response.context['messages_list'])
