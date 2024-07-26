from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from datetime import timedelta

class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_login_no_token(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Invalid credentials'})

    def test_login_invalid_username(self):
        response = self.client.post('/api/login/', {'username': 'invaliduser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Invalid credentials'})

    def test_login_invalid_password(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Invalid credentials'})

    def test_login_valid_credentials(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertIn('user', response.json())

    def test_login_existing_token(self):
        response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['token'], self.token.key)

    def test_signup_valid_data(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'role': 'admin'
        }
        response = self.client.post('/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], data['username'])
        self.assertEqual(response.data['user']['email'], data['email'])

    def test_signup_invalid_data_missing_username(self):
        data = {
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post('/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_signup_invalid_data_missing_password(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com'
        }
        response = self.client.post('/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_signup_invalid_data_duplicate_username(self):
        data = {
            'username': 'testuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'role': 'admin'
        }
        response = self.client.post('/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')

    def test_signup_invalid_data_invalid_email(self):
        data = {
        "username": "newuser",
        "password": "newpassword",
        "email": "newuser@example.com",
        "role": "admin"
    }
        response = self.client.post('/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')

    def test_token_authentication_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/test-token/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"passed for": "testuser@example.com"})

    def test_token_authentication_no_token(self):
        response = self.client.get('/test-token/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Authentication credentials were not provided."})

    def test_token_authentication_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.get('/test-token/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid token."})

    def test_token_authentication_expired_token(self):
        self.token.created = self.token.created - timedelta(days=30)
        self.token.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/test-token/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid token."})

    def test_token_authentication_unexpected_error(self):
        # Mocking an unexpected error
        def mock_get_user_email(self):
            raise Exception("Unexpected error")

        self.user.email = mock_get_user_email
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/test-token/')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Internal Server Error"})
