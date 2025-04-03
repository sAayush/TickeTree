from rest_framework import serializers
from .models import Ticket, TicketTransaction
from movies.serializers import MovieSerializer
from events.serializers import EventSerializer, ShowSerializer

class TicketTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTransaction
        fields = ['id', 'transaction_type', 'amount', 'blockchain_transaction_hash', 'created_at']
        read_only_fields = ['id', 'created_at']

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
            'used_at', 'cancelled_at', 'transactions'
        ]
        read_only_fields = [
            'id', 'user', 'blockchain_ticket_id', 'blockchain_transaction_hash',
            'created_at', 'updated_at', 'used_at', 'cancelled_at', 'transactions'
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