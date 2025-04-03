from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, TicketTransactionViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'transactions', TicketTransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
] 