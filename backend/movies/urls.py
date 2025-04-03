from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MovieViewSet, GenreViewSet, LanguageViewSet,
    PersonViewSet, MovieCastViewSet, MovieCrewViewSet,
    ReviewViewSet, ShowViewSet
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'persons', PersonViewSet, basename='person')
router.register(r'cast', MovieCastViewSet, basename='cast')
router.register(r'crew', MovieCrewViewSet, basename='crew')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'shows', ShowViewSet, basename='show')

urlpatterns = [
    path('', include(router.urls)),
]
