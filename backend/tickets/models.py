from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import UserProfile
from movies.models import Movie
from events.models import Event, Show

class Ticket(models.Model):
    # Basic Information
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=50)  # Can be 'movie', 'event', etc.
    status = models.CharField(max_length=50)  # Can be 'pending', 'confirmed', 'used', 'cancelled', 'refunded'
    
    # Event/Movie Reference
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    
    # Ticket Details
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=1)
    
    # Blockchain Integration
    blockchain_ticket_id = models.CharField(max_length=100, null=True, blank=True)
    blockchain_transaction_hash = models.CharField(max_length=100, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    used_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.ticket_type == 'movie':
            return f"Movie Ticket - {self.movie.title} - {self.seat_number}"
        else:
            return f"Event Ticket - {self.event.title} - {self.seat_number}"

    def save(self, *args, **kwargs):
        # Ensure either movie or event is set, but not both
        if not (self.movie is None) ^ (self.event is None):
            raise ValueError("Ticket must be associated with either a movie or an event, but not both")
        super().save(*args, **kwargs)

class TicketTransaction(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50)  # Can be 'purchase', 'refund', 'cancellation'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    blockchain_transaction_hash = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.ticket} - {self.amount}"
