# inventory/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()

class ProductViewSetTests(APITestCase):

    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username='adminuser', password='adminpass', email='admin@example.com', role='admin'
        )

        # Create an ordinary user
        self.ordinary_user = User.objects.create_user(
            username='ordinaryuser', password='ordinarypass', email='ordinary@example.com', role='user'
        )

        # Create some products with quantity
        self.product1 = Product.objects.create(name='Product1', description='Description1', price=10, quantity=100)
        self.product2 = Product.objects.create(name='Product2', description='Description2', price=20, quantity=200)

    def test_admin_can_create_product(self):
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('product-list')
        data = {'name': 'Product3', 'description': 'Description3', 'price': 30, 'quantity': 300}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_admin_can_update_product(self):
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('product-detail', args=[self.product1.id])
        data = {'name': 'Updated Product1', 'description': 'Updated Description1', 'price': 15, 'quantity': 150}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_admin_can_delete_product(self):
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('product-detail', args=[self.product1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()

    def test_ordinary_user_cannot_create_product(self):
        self.client.login(username='ordinaryuser', password='ordinarypass')
        url = reverse('product-list')
        data = {'name': 'Product3', 'description': 'Description3', 'price': 30, 'quantity': 300}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_ordinary_user_cannot_update_product(self):
        self.client.login(username='ordinaryuser', password='ordinarypass')
        url = reverse('product-detail', args=[self.product1.id])
        data = {'name': 'Updated Product1', 'description': 'Updated Description1', 'price': 15, 'quantity': 150}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_ordinary_user_cannot_delete_product(self):
        self.client.login(username='ordinaryuser', password='ordinarypass')
        url = reverse('product-detail', args=[self.product1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_any_user_can_view_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.client.logout()

    def test_unauthenticated_user_can_view_products(self):
        self.client.logout()
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
