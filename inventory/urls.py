# inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet



router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
#     
#     
#      path('report/low_stock/', LowStockReportView.as_view(), name='low_stock_report'),
#     path('report/sales/', SalesReportView.as_view(), name='sales_report'),

]
