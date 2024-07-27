from django.shortcuts import render

# Create your views here.
# reports/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum, F
from datetime import datetime, timedelta
from inventory.models import Product
from orders.models import OrderItem
from .serializers import LowStockProductSerializer, SalesReportSerializer

@api_view(['GET'])
@permission_classes([IsAdminUser])
def low_stock_products(request):
    low_stock_products = Product.objects.filter(quantity__lt=10)
    serializer = LowStockProductSerializer(low_stock_products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def sales_report(request, period):
    today = datetime.now().date()
    if period == 'day':
        start_date = today - timedelta(days=1)
    elif period == 'week':
        start_date = today - timedelta(weeks=1)
    elif period == 'month':
        start_date = today - timedelta(days=30)
    else:
        return Response({'error': 'Invalid period'}, status=status.HTTP_400_BAD_REQUEST)
    
    sales_data = OrderItem.objects.filter(order__created_at__gte=start_date).annotate(
        date=F('order__created_at__date')
    ).values('date').annotate(
        total_sales=Sum(F('quantity') * F('product__price'))
    ).values('date', 'total_sales')
    
    serializer = SalesReportSerializer(sales_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
