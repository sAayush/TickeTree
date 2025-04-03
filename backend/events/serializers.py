from rest_framework import serializers
from .models import Event, Show, EventCategory
from accounts.serializers import HostUserSerializer

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    shows = ShowSerializer(many=True, read_only=True)
    categories = EventCategorySerializer(many=True, read_only=True)
    host = HostUserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('host',)

class EventCreateSerializer(serializers.ModelSerializer):
    shows = ShowSerializer(many=True, required=False)
    category_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('host',)

    def create(self, validated_data):
        shows_data = validated_data.pop('shows', [])
        category_ids = validated_data.pop('category_ids', [])
        
        event = Event.objects.create(**validated_data)
        
        # Create shows
        for show_data in shows_data:
            Show.objects.create(event=event, **show_data)
        
        # Add categories
        if category_ids:
            event.categories.set(category_ids)
        
        return event 