from rest_framework import serializers
from .models import Movie, Genre, Language, Person, MovieCast, MovieCrew, Review, Show

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'code']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'bio', 'date_of_birth', 'image']

class MovieCastSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    person_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MovieCast
        fields = ['id', 'person', 'person_id', 'character_name', 'is_lead', 'order']

class MovieCrewSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    person_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MovieCrew
        fields = ['id', 'person', 'person_id', 'role', 'specific_role']

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_email', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user']

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'
        ref_name = 'MovieShow'

    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be after start time")
        if data['available_seats'] > data['total_seats']:
            raise serializers.ValidationError("Available seats cannot be more than total seats")
        return data

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    cast = MovieCastSerializer(many=True, read_only=True)
    crew = MovieCrewSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    shows = ShowSerializer(many=True, read_only=True)
    
    # Write-only fields for managing relationships
    genre_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    language_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'tagline', 'description',
            'duration', 'release_date', 'genres', 'genre_ids',
            'languages', 'language_ids', 'certification',
            'status', 'poster', 'banner', 'trailer_url',
            'rating', 'vote_count', 'budget', 'box_office',
            'is_featured', 'cast', 'crew', 'reviews', 'shows',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        genre_ids = validated_data.pop('genre_ids', [])
        language_ids = validated_data.pop('language_ids', [])
        
        movie = Movie.objects.create(**validated_data)
        
        # Add genres and languages
        if genre_ids:
            movie.genres.set(genre_ids)
        if language_ids:
            movie.languages.set(language_ids)
            
        return movie

    def update(self, instance, validated_data):
        genre_ids = validated_data.pop('genre_ids', None)
        language_ids = validated_data.pop('language_ids', None)
        
        # Update the movie instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update relationships if provided
        if genre_ids is not None:
            instance.genres.set(genre_ids)
        if language_ids is not None:
            instance.languages.set(language_ids)
            
        return instance

class MovieListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    genres = GenreSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'release_date', 'poster',
            'genres', 'languages', 'certification',
            'status', 'rating', 'is_featured'
        ] 