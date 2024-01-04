from django.test import TestCase, Client
from rest_framework import status
from myuser.models import MyUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

class SignUpLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view(self):
        # Test signup with valid data
        response = self.client.post('/api/auth/signup/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test signup with missing data
        response = self.client.post('/api/auth/signup/', {'username': 'testuser1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view(self):
        # Create a user for testing
        user = MyUser(username='new_testuser', password=make_password('new_testuser'))
        user.save()

        # Test login with valid credentials
        response = self.client.post('/api/auth/login/', {'username': 'new_testuser', 'password': 'new_testuser'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        # Test login with invalid credentials
        response = self.client.post('/api/auth/login/', {'username': 'new_testuser', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_token_generation(self):
        # Create a user for testing
        user = MyUser(username='token_testuser', password=make_password('testpassword'))
        user.save()

        response = self.client.post('/api/auth/login/', {'username': 'token_testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        token_key = response.data['token']

        # Retrieve the token from the database and verify it matches
        token = Token.objects.get(user=user)
        self.assertEqual(token.key, token_key)
