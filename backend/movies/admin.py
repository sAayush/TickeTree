from django.contrib import admin
from .models import Movie, Genre, Language, Person, MovieCast, MovieCrew, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'certification', 'status', 'rating')
    list_filter = ('status', 'certification', 'genres', 'languages')
    search_fields = ('title', 'original_title', 'description')
    date_hierarchy = 'release_date'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    search_fields = ('name',)

@admin.register(MovieCast)
class MovieCastAdmin(admin.ModelAdmin):
    list_display = ('movie', 'person', 'character_name', 'is_lead')
    list_filter = ('is_lead', 'movie')

@admin.register(MovieCrew)
class MovieCrewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'person', 'role')
    list_filter = ('role', 'movie')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'movie')
