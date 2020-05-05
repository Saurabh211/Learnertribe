from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authuser.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('institute', 'class_room', 'full_name','mobile_number','is_verified','created_at')
    list_filter=('institute','class_room','full_name','mobile_number','is_verified')
admin.site.register(User,UserAdmin)