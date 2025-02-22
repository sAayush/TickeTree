from django.db import models
from accounts.models import HostProfile
from django.utils.timezone import now 
# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateTimeField(default=now)
    venue = models.CharField(max_length=255)
    event_description = models.TextField()
    total_tickets = models.PositiveIntegerField(default=0)
    available_tickets = models.PositiveIntegerField(default=0)
    event_host = models.ForeignKey(HostProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.event_name} - {self.venue} - {self.event_date.strftime('%Y-%m-%d %H:%M')}"

