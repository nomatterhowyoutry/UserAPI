from django.contrib.auth import get_user_model

from rest_framework_jwt.settings import api_settings
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from posts.models import Post

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class PostsAPITestCase(APITestCase):

    def setUp(self):
        user_obj = User(username='TestUser', email='Test@mail.com')
        user_obj.set_password("rand32897ompa22")
        user_obj.save()
        post_obj = Post.objects.create(
            user=user_obj,
            title='Test Title',
            content='Some Test Content'
        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_get_list(self):
        data = {}
        url = reverse("post-create")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {"title": "random title", "content": "random content"}
        url = reverse("post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        post = Post.objects.first()
        data = {}
        url = post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        post = Post.objects.first()
        url = post.get_api_url()
        data = {"title": "random title", "content": "random content"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        post = Post.objects.first()
        url = post.get_api_url()
        data = {"title": "random title", "content": "random content"}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item_with_user(self):
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
        data = {"title": "random title", "content": "random content"}
        url = reverse("post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username='TestUser2')
        post = Post.objects.create(
                user=owner,
                title='random title',
                content='random content'
                )
        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
        url = post.get_api_url()
        data = {"title": "random title 2", "content": "random content 2"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username': 'TestUser',
            'password': 'rand32897ompa22'
        }
        url = reverse("login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            post = Post.objects.first()
            url = post.get_api_url()
            data = {"title": "random title", "content": "random content"}
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)