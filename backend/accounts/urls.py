from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
