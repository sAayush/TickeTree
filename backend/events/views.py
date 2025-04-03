from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Event, Show, EventCategory
from .serializers import (
    EventSerializer, 
    ShowSerializer, 
    EventCategorySerializer,
    EventCreateSerializer
)
from accounts.models import HostProfile

# Create your views here.

class IsHostUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'HOST'

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventCreateSerializer
        return EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsHostUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        host_profile = HostProfile.objects.get(user=self.request.user)
        serializer.save(host=host_profile)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_events = Event.objects.filter(is_featured=True)
        serializer = self.get_serializer(featured_events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_events(self, request):
        if not request.user.is_authenticated or request.user.user_type != 'HOST':
            return Response(
                {"error": "Not authorized"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        host_profile = HostProfile.objects.get(user=request.user)
        events = Event.objects.filter(host=host_profile)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsHostUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        event = get_object_or_404(Event, pk=self.kwargs.get('event_pk'))
        if event.host.user != self.request.user:
            raise permissions.PermissionDenied()
        serializer.save(event=event)

class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
