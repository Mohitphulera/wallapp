import json
from unittest.mock import patch
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from posts.models import Post

from .models import User, send_success_email


class UserTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_creation(self):
        self.client.post(
            '/users/', {'username': 'test-user', 'password': 'mock123it', 'email': 'me@mail.com'})
        self.assertTrue(User.objects.filter(username='test-user').exists())

    def test_user_login(self):
        user = User.objects.create_user(
            username='test-user', password='mock123it', email='me@mail.com')
        self.client.post(
            '/auth/', {'username': 'test-user', 'password': 'mock123it'})
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_user_logout(self):
        user = User.objects.create_user(
            username='test-user', password='mock123it', email='me@mail.com')
        response = self.client.post(
            '/auth/', {'username': 'test-user', 'password': 'mock123it'})
        token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.client.delete('/auth/')
        self.assertFalse(Token.objects.filter(user=user).exists())

    @patch('django.core.mail.EmailMessage.send')
    def test_welcome_email(self, mockEmail):
        post_save.connect(send_success_email, sender=User)
        user = User.objects.create_user(
            username='test-user', password='mock123it', email='me@mail.com')
        self.assertTrue(mockEmail.called)
        self.assertTrue(mockEmail.call_count, 1)
        mockEmail.reset_mock()
        user.save()
        self.assertFalse(mockEmail.called)
