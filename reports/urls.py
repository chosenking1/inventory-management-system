
from django.urls import path
from .views import low_stock_products, sales_report

urlpatterns = [
    path('low-stock-products/', low_stock_products, name='low-stock-products'),
    path('sales-report/<str:period>/', sales_report, name='sales-report'),
]
