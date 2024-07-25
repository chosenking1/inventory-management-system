from django.test import TestCase

# inventory/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Product, Order

User = get_user_model()

class InventoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.user = User.objects.create_user(username='user', password='user123', role='user')
        self.product = Product.objects.create(name='Product1', description='Description1', quantity=5, price=100)

    def test_register(self):
        response = self.client.post('/api/register/', {'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com', 'role': 'user'})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post('/api/login/', {'username': 'user', 'password': 'user123'})
        self.assertEqual(response.status_code, 200)

    def test_add_product_as_admin(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post('/api/products/', {'name': 'Product2', 'description': 'Description2', 'quantity': 10, 'price': 50})
        self.assertEqual(response.status_code, 201)

    def test_add_product_as_user(self):
        self.client.login(username='user', password='user123')
        response = self.client.post('/api/products/', {'name': 'Product2', 'description': 'Description2', 'quantity': 10, 'price': 50})
        self.assertEqual(response.status_code, 403)

    def test_create_order(self):
        self.client.login(username='user', password='user123')
        response = self.client.post('/api/orders/', {'user': self.user.id, 'items': [{'product': self.product.id, 'quantity': 2}]})
        self.assertEqual(response.status_code, 201)

    def test_low_stock_report(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/api/report/low_stock/')
        self.assertEqual(response.status_code, 200)

    def test_sales_report(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/api/report/sales/')
        self.assertEqual(response.status_code, 200)

