from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import HostProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'user_type')
        read_only_fields = ('user_type',)

class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, help_text="User's first name")
    last_name = serializers.CharField(required=True, help_text="User's last name")
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'help_text': "User's email address"},
            'username': {'help_text': "User's username"}
        }

class HostProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostProfile
        fields = ('organization_name', 'address', 'contact_number', 'website', 'description')

class HostUserSerializer(serializers.ModelSerializer):
    host_profile = HostProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'user_type', 'host_profile')
        read_only_fields = ('user_type',)

class RegisterHostSerializer(serializers.ModelSerializer):
    host_profile = HostProfileSerializer()
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'host_profile')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        host_profile_data = validated_data.pop('host_profile')
        user = User.objects.create_user(**validated_data, user_type='HOST')
        HostProfile.objects.create(user=user, **host_profile_data)
        return user