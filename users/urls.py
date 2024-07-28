from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import login, signup, test_token, logout





urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('test_token/', test_token, name='test_token'),
    path('logout/', logout, name='logout'),
]
