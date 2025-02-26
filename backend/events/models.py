from django.db import models
from accounts.models import UserProfile, HostProfile

class Event(models.Model):
    host = models.ForeignKey(HostProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=255)
    total_tickets = models.IntegerField()
    available_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    smart_contract_address = models.CharField(max_length=42, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title