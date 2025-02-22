from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
        if data['available_tickets'] > data['total_tickets']:
            raise serializers.ValidationError(
                "Available tickets cannot exceed total tickets."
            )
        return data