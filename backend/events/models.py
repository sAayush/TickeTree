from django.db import models
from accounts.models import UserProfile, HostProfile

class Event(models.Model):
    host = models.ForeignKey(HostProfile, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100)  # Concert, Theater, Sports, etc.
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='DRAFT')  # Simplified status field
    banner_image = models.ImageField(upload_to='event_banners/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Show(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='shows')
    show_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='UPCOMING')  # Simplified status field
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.event.title} - {self.show_date}"

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    events = models.ManyToManyField(Event, related_name='categories')

    def __str__(self):
        return self.name