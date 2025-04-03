from rest_framework import serializers
from .models import Ticket, TicketTransaction
from movies.serializers import MovieSerializer
from events.serializers import EventSerializer, ShowSerializer
from movies.models import Show
from django.utils import timezone

class TicketTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTransaction
        fields = ['id', 'ticket', 'transaction_type', 'amount', 'blockchain_transaction_hash', 'created_at']
        read_only_fields = ['blockchain_transaction_hash', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    show = ShowSerializer(read_only=True)
    transactions = TicketTransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'user', 'ticket_type', 'status', 'movie', 'event', 'show',
            'seat_number', 'price', 'quantity', 'blockchain_ticket_id',
            'blockchain_transaction_hash', 'created_at', 'updated_at',
            'used_at', 'cancelled_at', 'transactions', 'qr_code', 'qr_data',
            'transfer_history'
        ]
        read_only_fields = [
            'id', 'user', 'blockchain_ticket_id', 'blockchain_transaction_hash',
            'created_at', 'updated_at', 'used_at', 'cancelled_at', 'transactions',
            'qr_code', 'qr_data', 'transfer_history'
        ]

    def validate(self, data):
        if data.get('ticket_type') == 'movie' and not data.get('movie'):
            raise serializers.ValidationError("Movie ticket must have a movie")
        if data.get('ticket_type') == 'event' and not data.get('event'):
            raise serializers.ValidationError("Event ticket must have an event")
        return data

class TicketPurchaseSerializer(serializers.Serializer):
    ticket_type = serializers.CharField()  # 'movie' or 'event'
    movie_id = serializers.IntegerField(required=False)
    event_id = serializers.IntegerField(required=False)
    show_id = serializers.IntegerField(required=False)
    seat_number = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(default=1)

    def validate(self, data):
        if data['ticket_type'] == 'movie' and not data.get('movie_id'):
            raise serializers.ValidationError("Movie ticket must have a movie_id")
        if data['ticket_type'] == 'event' and not data.get('event_id'):
            raise serializers.ValidationError("Event ticket must have an event_id")
        if data['ticket_type'] == 'event' and not data.get('show_id'):
            raise serializers.ValidationError("Event ticket must have a show_id")
        return data 

class TicketBookingSerializer(serializers.Serializer):
    show_id = serializers.IntegerField()
    seat_numbers = serializers.ListField(child=serializers.IntegerField())
    user_wallet_address = serializers.CharField(max_length=42)

    def validate(self, data):
        show = Show.objects.filter(id=data['show_id']).first()
        if not show:
            raise serializers.ValidationError("Show not found")
        
        if show.show_date < timezone.now().date():
            raise serializers.ValidationError("Show date has passed")
        
        # Check if seats are available
        for seat_number in data['seat_numbers']:
            if seat_number > show.total_seats:
                raise serializers.ValidationError(f"Seat {seat_number} does not exist")
            
            if Ticket.objects.filter(show=show, seat_number=seat_number).exists():
                raise serializers.ValidationError(f"Seat {seat_number} is already booked")
        
        return data

class TicketVerificationSerializer(serializers.Serializer):
    token_id = serializers.CharField()
    user_wallet_address = serializers.CharField(max_length=42)

class QRCodeVerificationSerializer(serializers.Serializer):
    qr_data = serializers.CharField()

class TicketTransferSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    new_owner_wallet_address = serializers.CharField(max_length=42)

    def validate(self, data):
        try:
            ticket = Ticket.objects.get(id=data['ticket_id'])
            if ticket.is_used:
                raise serializers.ValidationError("Cannot transfer used ticket")
            if ticket.user != self.context['request'].user:
                raise serializers.ValidationError("You are not the owner of this ticket")
        except Ticket.DoesNotExist:
            raise serializers.ValidationError("Ticket not found")
        return data