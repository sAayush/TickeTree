from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)  # For language codes like 'en', 'es', etc.
    
    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='person_images/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    CERTIFICATION_CHOICES = [
        ('U', 'Universal'),
        ('UA', 'Universal with Adult Supervision'),
        ('A', 'Adult'),
        ('S', 'Special Category')
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('running', 'Now Running'),
        ('finished', 'Finished')
    ]

    # Basic Information
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    tagline = models.CharField(max_length=500, blank=True)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    
    # Classifications
    genres = models.ManyToManyField(Genre)
    languages = models.ManyToManyField(Language)
    certification = models.CharField(max_length=2, choices=CERTIFICATION_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    
    # Media
    poster = models.ImageField(upload_to='movie_posters/')
    banner = models.ImageField(upload_to='movie_banners/', null=True, blank=True)
    trailer_url = models.URLField(blank=True)
    
    # Metrics
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True
    )
    vote_count = models.IntegerField(default=0)
    
    # Additional Info
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    box_office = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, related_name='cast', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255)
    is_lead = models.BooleanField(default=False)
    order = models.IntegerField(default=0)  # For ordering cast members

    class Meta:
        ordering = ['order']
        unique_together = ['movie', 'person', 'character_name']

    def __str__(self):
        return f"{self.person.name} as {self.character_name} in {self.movie.title}"

class MovieCrew(models.Model):
    ROLE_CHOICES = [
        ('director', 'Director'),
        ('producer', 'Producer'),
        ('writer', 'Writer'),
        ('music_director', 'Music Director'),
        ('cinematographer', 'Cinematographer'),
        ('editor', 'Editor'),
        ('other', 'Other')
    ]

    movie = models.ForeignKey(Movie, related_name='crew', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    specific_role = models.CharField(max_length=255, blank=True)  # For 'other' roles

    class Meta:
        unique_together = ['movie', 'person', 'role']

    def __str__(self):
        return f"{self.person.name} as {self.get_role_display()} in {self.movie.title}"

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.UserProfile', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['movie', 'user']

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.email}"
