# reports/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from inventory.models import Product
from orders.models import Order, OrderItem

User = get_user_model()

class ReportTests(APITestCase):

    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username='adminuser', password='adminpass', email='admin@example.com', role='admin'
        )

        # Create an ordinary user
        self.ordinary_user = User.objects.create_user(
            username='ordinaryuser', password='ordinarypass', email='ordinary@example.com', role='user'
        )

        # Create products
        self.product1 = Product.objects.create(name='Product1', description='Description1', price=10, quantity=5)
        self.product2 = Product.objects.create(name='Product2', description='Description2', price=20, quantity=20)

        # Create orders
        self.order1 = Order.objects.create(user=self.ordinary_user)
        self.order_item1 = OrderItem.objects.create(order=self.order1, product=self.product1, quantity=2)

        self.order2 = Order.objects.create(user=self.ordinary_user)
        self.order_item2 = OrderItem.objects.create(order=self.order2, product=self.product2, quantity=3)

    def test_admin_can_view_low_stock_products(self):
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('low-stock-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_ordinary_user_cannot_view_low_stock_products(self):
        self.client.login(username='ordinaryuser', password='ordinarypass')
        url = reverse('low-stock-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_admin_can_view_sales_report(self):
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('sales-report', args=['day'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_ordinary_user_cannot_view_sales_report(self):
        self.client.login(username='ordinaryuser', password='ordinarypass')
        url = reverse('sales-report', args=['day'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
