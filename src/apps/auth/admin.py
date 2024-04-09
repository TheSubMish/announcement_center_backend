from django.contrib import admin
from .models import User, Device
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','is_active','is_staff','date_joined']
    ordering = ('-date_joined',)
    search_fields = ['username','email']

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id','device_ip','device_type','device_os','browser_type']
    ordering = ('-created_at',)
    search_fields = ['device_ip','device_type']