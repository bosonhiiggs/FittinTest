from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

client = APIClient()


class AuthTests(APITestCase):
    def setUp(self):
        self.client = client
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
        )

        self.url_login = reverse('myauth:token-login')
        self.url_register = reverse('myauth:register')
        self.url_refresh = reverse('myauth:token-refresh')

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
        }
        response = self.client.post(self.url_register, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_login_user(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.url_login, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_user(self):
        login_data = {
            'username': self.username,
            'password': self.password,
        }
        login_response = self.client.post(self.url_login, login_data, format='json')
        refresh_token = login_response.data['refresh']
        data = {
            'refresh': refresh_token
        }
        response = self.client.post(self.url_refresh, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


