from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase

class UserAuthTests(APITestCase):
    
    def setUp(self):
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(
            username='testuser', password='testpassword', email='testuser@example.com', role='user')
        self.test_admin = self.user_model.objects.create_user(
            username='adminuser', password='adminpassword', email='adminuser@example.com', role='admin')
        self.client = self.client_class()

    def test_signup_valid_user(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'role': 'user'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')

    def test_signup_valid_admin(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newadmin',
            'password': 'newadminpassword',
            'email': 'newadmin@example.com',
            'role': 'admin'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newadmin')
        self.assertEqual(response.data['user']['email'], 'newadmin@example.com')
        self.assertEqual(response.data['user']['role'], 'admin')

    def test_signup_invalid(self):
        response = self.client.post(reverse('signup'), {
            'username': '',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'role': 'user'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_login_valid_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_login_valid_admin(self):
        response = self.client.post(reverse('login'), {
            'username': 'adminuser',
            'password': 'adminpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['role'], 'admin')

    def test_login_invalid_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'invaliduser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'Invalid credentials'})

    def test_login_invalid_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'invalidpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'Invalid credentials'})

    def test_logout_valid(self):
        token = Token.objects.create(user=self.test_user)
        self.client.force_authenticate(user=self.test_user, token=token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"detail": "Successfully logged out."})

    def test_logout_no_token(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "Authentication credentials were not provided."})

    def test_logout_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "Invalid token."})

    def test_token_authentication_success(self):
        token = Token.objects.create(user=self.test_user)
        self.client.force_authenticate(user=self.test_user, token=token.key)
        response = self.client.get(reverse('test_token'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"passed for": "testuser@example.com"})

 