# inventory/views.py
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users with role 'admin' to edit it.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to users with role 'admin'.
        return request.user and request.user.role == 'admin'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
