from django.urls import path
from .views import *

urlpatterns = [
    # Movie URLs
    path('movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    
    # Genre and Language URLs
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('languages/', LanguageListView.as_view(), name='language-list'),
    
    # Cast and Crew URLs
    path('movies/<int:movie_id>/cast/', MovieCastView.as_view(), name='movie-cast'),
    path('movies/<int:movie_id>/crew/', MovieCrewView.as_view(), name='movie-crew'),
    
    # Utility URLs
    path('certifications/', CertificationListView.as_view(), name='certification-list'),
    path('movie-statuses/', MovieStatusListView.as_view(), name='movie-status-list'),
]
