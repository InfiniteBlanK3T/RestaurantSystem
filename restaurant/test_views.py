from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class CustomTokenObtainPairViewTest(APITestCase):
    def setUp(self):
        # Create test users
        self.customer_user = User.objects.create_user(
            username='customer',
            password='customer_password',
            role='customer'
        )
        self.staff_user = User.objects.create_user(
            username='staff',
            password='staff_password',
            role='staff'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin_password',
            role='admin'
        )

    def test_customer_token_obtain(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'customer',
            'password': 'customer_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('user_role', response.data)
        self.assertEqual(response.data['user_role'], 'customer')

    def test_staff_token_obtain(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'staff',
            'password': 'staff_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('user_role', response.data)
        self.assertEqual(response.data['user_role'], 'staff')

    def test_admin_token_obtain(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 'admin_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('user_role', response.data)
        self.assertEqual(response.data['user_role'], 'admin')

    def test_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 'wrong_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)