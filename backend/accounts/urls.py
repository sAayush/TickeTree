from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginUserView, 
    RegisterUserView, 
    UserListCreateView, 
    UserDetailView,
    LoginHostView,
    RegisterHostView,
    RefreshTokenView
)

urlpatterns = [
    path("account/register/", RegisterUserView.as_view(), name="register"),
    path('account/users/', UserListCreateView.as_view(), name='user-list'),
    path('account/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('account/login/', LoginUserView.as_view(), name='login'),
    path('account/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('host/login/', LoginHostView.as_view(), name='host-login'),
    path('host/register/', RegisterHostView.as_view(), name='host-register'),
]
