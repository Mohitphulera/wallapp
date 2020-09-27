import json

from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import User

from .models import Post
from .serializers import PostSerializer


class PostTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='pass123', email='mohit@gmail.com')
        self.client = APIClient()
        response = self.client.post(
            '/auth/', {'username': 'user', 'password': 'pass123'})
        self.token = json.loads(response.content)['token']

    def test_listing(self):
        Post.objects.create(message='Hello!', author=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/posts/')
        posts = json.loads(response.content)
        self.assertEqual(len(posts), 1)


    def test_posting(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        post = 'Making a post on the wall!'
        self.client.post('/posts/', {'message': post})
        self.assertTrue(Post.objects.filter(message=post).exists())


    def test_update(self):
        post = 'Making a post on the wall!'
        instance = Post.objects.create(message=post, author=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        new_post = 'Updating a post on the wall!'
        self.client.patch('/posts/%i/' % instance.id, {'message': new_post})
        self.assertTrue(Post.objects.filter(message=new_post).exists())


    def test_full_update(self):
        post = 'Making a post on the wall!'
        instance = Post.objects.create(message=post, author=self.user)
        post_data = PostSerializer(instance).data
        new_message = 'Updating a post on the wall!'
        post_data['message'] = new_message
        post_data['author'] = post_data['author']['username']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.client.put('/posts/%i/' % instance.id, post_data)
        self.assertTrue(Post.objects.filter(message=new_message).exists())



