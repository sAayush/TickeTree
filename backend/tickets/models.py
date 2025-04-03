from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import UserProfile
from movies.models import Movie, Show
from events.models import Event
from django.conf import settings
from django.utils import timezone

class Ticket(models.Model):
    # Basic Information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_tickets')
    ticket_type = models.CharField(max_length=50)  # Can be 'movie', 'event', etc.
    status = models.CharField(max_length=50)  # Can be 'pending', 'confirmed', 'used', 'cancelled', 'refunded'
    
    # Event/Movie Reference
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets')
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    
    # Ticket Details
    seat_number = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    # Blockchain Integration
    token_id = models.CharField(max_length=100, unique=True)
    transaction_hash = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    used_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # QR Code
    qr_code = models.TextField(null=True, blank=True)  # Store base64 QR code
    qr_data = models.TextField(null=True, blank=True)  # Store QR code data
    transfer_history = models.JSONField(default=list, blank=True)  # Store transfer history

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

    def generate_qr_code(self):
        from .services import QRCodeService
        qr_service = QRCodeService()
        
        ticket_data = {
            'token_id': self.token_id,
            'show_id': self.show.id,
            'seat_number': self.seat_number,
            'user_wallet_address': self.user.wallet_address
        }
        
        result = qr_service.generate_ticket_qr(ticket_data)
        if result['success']:
            self.qr_code = result['qr_code']
            self.qr_data = result['qr_data']
            self.save()
        return result

    def verify_on_blockchain(self):
        from .services import BlockchainService
        blockchain_service = BlockchainService()
        result = blockchain_service.verify_ticket(int(self.token_id))
        if result['success']:
            self.is_used = result['is_used']
            self.save()
        return result

    def use_ticket(self):
        if self.is_used:
            return False, "Ticket already used"
        
        from .services import BlockchainService
        blockchain_service = BlockchainService()
        result = blockchain_service.use_ticket(
            int(self.token_id),
            self.user.wallet_address
        )
        
        if result['success']:
            self.is_used = True
            self.used_at = timezone.now()
            self.save()
            return True, "Ticket used successfully"
        return False, result['error']

    def transfer_ticket(self, new_owner_wallet_address):
        if self.is_used:
            return False, "Cannot transfer used ticket"
        
        from .services import BlockchainService
        blockchain_service = BlockchainService()
        
        # Transfer on blockchain
        result = blockchain_service.transfer_ticket(
            int(self.token_id),
            self.user.wallet_address,
            new_owner_wallet_address
        )
        
        if not result['success']:
            return False, result['error']
        
        # Update transfer history
        transfer_record = {
            'from_wallet': self.user.wallet_address,
            'to_wallet': new_owner_wallet_address,
            'timestamp': timezone.now().isoformat(),
            'transaction_hash': result['transaction_hash']
        }
        
        self.transfer_history.append(transfer_record)
        self.save()
        
        return True, "Ticket transferred successfully"

class TicketTransaction(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=50)  # Can be 'purchase', 'refund', 'cancellation'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    blockchain_transaction_hash = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.ticket} - {self.amount}"
