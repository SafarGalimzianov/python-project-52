from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.user), 'Test User')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.check_password('testpass123'))


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )

    def test_user_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_create(self):
        user_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(
            reverse('users_create'),
            user_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        self.client.login(username='testuser', password='testpass123')

        updated_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'updatedpass123',
            'password2': 'updatedpass123'
        }

        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user.id}),
            updated_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_user_delete(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())


class UserDeletePermissionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='user1pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='user2pass123'
        )

    def test_user_can_only_delete_own_account(self):
        self.client.login(username='user1', password='user1pass123')

        response = self.client.get(
            reverse('users_delete', kwargs={'pk': self.user2.id}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='user2').exists())

        response = self.client.get(
            reverse('users_delete', kwargs={'pk': self.user1.id}),
            follow=True
        )
        if response.status_code == 200:
            response = self.client.post(
                reverse('users_delete', kwargs={'pk': self.user1.id}),
                follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='user1').exists())


class UserDeleteWithTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
    def test_delete_user_with_tasks(self):
        status = Status.objects.create(name='Test Status')
        Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=status,
            creator=self.user,
            executor=self.user
        )

        response = self.client.get(
            reverse('users_delete', kwargs={'pk': self.user.id}),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('users'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

        self.client.post(
            reverse('users_delete', kwargs={'pk': self.user.id}),
            follow=True
        )
        self.assertTrue(User.objects.filter(username='testuser').exists())
