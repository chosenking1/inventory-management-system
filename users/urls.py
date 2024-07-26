from django.urls import re_path, include
from rest_framework.routers import DefaultRouter
from .views import login, signup, test_token, logout





urlpatterns = [
    re_path('login', login),
    re_path('signup', signup),
    re_path('test_token', test_token),
    re_path('logout', logout),
]
