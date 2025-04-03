from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MovieViewSet, GenreViewSet, LanguageViewSet,
    MovieCastViewSet, MovieCrewViewSet, ShowViewSet
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'shows', ShowViewSet)

# Nested routes for cast and crew
movie_cast_router = DefaultRouter()
movie_cast_router.register(r'cast', MovieCastViewSet, basename='movie-cast')

movie_crew_router = DefaultRouter()
movie_crew_router.register(r'crew', MovieCrewViewSet, basename='movie-crew')

urlpatterns = [
    path('', include(router.urls)),
    path('movies/<int:movie_id>/', include(movie_cast_router.urls)),
    path('movies/<int:movie_id>/', include(movie_crew_router.urls)),
]
