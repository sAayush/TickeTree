from django.urls import path
from .views import *

urlpatterns = [
    path("account/register/", RegisterUserView.as_view(), name="register"),
    path('account/users/', UserListCreateView.as_view(), name='user-list'),
    path('account/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('account/login/', LoginUserView.as_view(), name='login'),
    path('account/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
