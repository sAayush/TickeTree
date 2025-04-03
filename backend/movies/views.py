from django.shortcuts import render
from rest_framework import generics, status, filters, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Movie, Genre, Language, Person, MovieCast, MovieCrew, Show
from .serializers import (
    MovieSerializer, MovieListSerializer, GenreSerializer,
    LanguageSerializer, PersonSerializer, MovieCastSerializer,
    MovieCrewSerializer, ShowSerializer
)
from utils.utils import create_response
from rest_framework.decorators import action

# Movie Views
class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'certification', 'genres', 'languages']
    search_fields = ['title', 'description']
    ordering_fields = ['release_date', 'rating']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MovieSerializer
        return MovieListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return create_response(
            status="success",
            message="Movies retrieved successfully",
            data=serializer.data
        )

    def create(self, request, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                status="success",
                message="Movie created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return create_response(
            status="error",
            message="Invalid data",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return create_response(
            status="success",
            message="Movie details retrieved successfully",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return create_response(
                status="success",
                message="Movie updated successfully",
                data=serializer.data
            )
        return create_response(
            status="error",
            message="Invalid data",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return create_response(
            status="success",
            message="Movie deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )

# Genre Views
class GenreListView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return create_response(
            status="success",
            message="Genres retrieved successfully",
            data=serializer.data
        )

# Language Views
class LanguageListView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return create_response(
            status="success",
            message="Languages retrieved successfully",
            data=serializer.data
        )

# Cast and Crew Management Views
class MovieCastView(generics.ListCreateAPIView):
    serializer_class = MovieCastSerializer

    def get_queryset(self):
        return MovieCast.objects.filter(movie_id=self.kwargs['movie_id'])

    def perform_create(self, serializer):
        serializer.save(movie_id=self.kwargs['movie_id'])

class MovieCrewView(generics.ListCreateAPIView):
    serializer_class = MovieCrewSerializer

    def get_queryset(self):
        return MovieCrew.objects.filter(movie_id=self.kwargs['movie_id'])

    def perform_create(self, serializer):
        serializer.save(movie_id=self.kwargs['movie_id'])

# Show Views
class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset.filter(show_date__gte=timezone.now().date())

    @action(detail=True, methods=['post'])
    def book_tickets(self, request, pk=None):
        show = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if not show.is_available():
            return Response(
                {'error': 'Show is not available for booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if show.available_seats < quantity:
            return Response(
                {'error': f'Only {show.available_seats} seats available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if show.update_available_seats(quantity):
            return Response({
                'message': f'Successfully booked {quantity} tickets',
                'show_id': show.id,
                'available_seats': show.available_seats
            })
        
        return Response(
            {'error': 'Failed to book tickets'},
            status=status.HTTP_400_BAD_REQUEST
        )

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = self.queryset
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=True, methods=['get'])
    def shows(self, request, pk=None):
        movie = self.get_object()
        shows = movie.shows.filter(show_date__gte=timezone.now().date())
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)
