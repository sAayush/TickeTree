from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, HostProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'get_user_type', 'get_is_verified', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('user_type', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type')}
        ),
    )

    def get_user_type(self, obj):
        return obj.get_user_type_display()
    get_user_type.short_description = "User Type"

    def get_is_verified(self, obj):
        return obj.is_verified
    get_is_verified.boolean = True 
    get_is_verified.short_description = "Verified"

admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(HostProfile)