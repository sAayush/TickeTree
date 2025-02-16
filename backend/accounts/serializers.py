from rest_framework import serializers
from .models import CustomUser, HostProfile

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'user_type', 'password')

class HostProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostProfile
        fields = '__all__'
