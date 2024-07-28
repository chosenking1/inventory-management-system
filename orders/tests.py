# orders/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Order, OrderItem
from inventory.models import Product

User = get_user_model()

class OrderViewSetTests(APITestCase):

    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username='adminuser', password='adminpass', email='admin@example.com', role='admin'
        )

        # Create an ordinary user
        self.ordinary_user = User.objects.create_user(
            username='ordinaryuser', password='ordinarypass', email='ordinary@example.com', role='user'
        )

        # Create a product
        self.product = Product.objects.create(name='Product1', description='Description1', price=10, quantity=100)

        # Create an order
        self.order = Order.objects.create(user=self.ordinary_user)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

    def test_admin_can_update_order_status(self):
        self.client.login(username='adminuser', password='adminpass')
        url = reverse('order-update-status', args=[self.order.id])
        data = {'status': 'completed'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_ordinary_user_cannot_update_order_status(self):
        self.client.login(username='ordinaryuser', password='ordinarypass')
        url = reverse('order-update-status', args=[self.order.id])
        data = {'status': 'completed'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
