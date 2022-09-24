from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ['password', 'uuid']
    search_fields = ['email']
    list_filter = ['is_active']
    list_display = ['email', 'phone_number', 'last_login', 'is_active']
