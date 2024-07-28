from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer
from rest_framework import viewsets, permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users with role 'admin'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateOrderSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        order = self.get_object()
        order_status = request.data.get('status')
        if order_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = order_status
        order.save()
        return Response({"status": order.status}, status=status.HTTP_200_OK)
