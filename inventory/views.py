# from django.shortcuts import render
# from django.db.models import Sum
# # Create your views here.
# # inventory/views.py
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import authenticate, login
# from .serializers import RegisterSerializer, LoginSerializer

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer

# class LoginView(APIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = authenticate(
#             request,
#             username=serializer.validated_data['username'],
#             password=serializer.validated_data['password']
#         )
#         if user:
#             login(request, user)
#             return Response({"detail": "Successfully logged in."}, status=status.HTTP_200_OK)
#         return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)


# # inventory/views.py
# from rest_framework import viewsets, permissions
# from .models import Product, Order
# from .serializers import ProductSerializer, OrderSerializer

# class IsAdminUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_staff

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get_permissions(self):
#         if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
#             self.permission_classes = [IsAdminUser,]
#         else:
#             self.permission_classes = [permissions.AllowAny,]
#         return super().get_permissions()

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def get_permissions(self):
#         if self.request.method in ['PUT', 'PATCH']:
#             self.permission_classes = [IsAdminUser,]
#         else:
#             self.permission_classes = [permissions.IsAuthenticated,]
#         return super().get_permissions()



# # inventory/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser
# from .models import Product, Order

# class LowStockReportView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         low_stock_products = Product.objects.filter(quantity__lt=10)
#         serializer = ProductSerializer(low_stock_products, many=True)
#         return Response(serializer.data)

# class SalesReportView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         sales_report = Order.objects.values('status', 'created_at__date').annotate(total_sales=Sum('items__quantity'))
#         return Response(sales_report)


