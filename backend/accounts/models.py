from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUser(AbstractBaseUser, PermissionsMixin):    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=30)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username']

    def __str__(self):
        return self.username
    
class HostProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="host_profile")
    organization_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    description = models.TextField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.organization_name