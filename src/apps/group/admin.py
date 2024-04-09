from django.contrib import admin
from .models import Group
# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_id','name','admin_id','created_at']
    ordering = ('-created_at',)
    search_fields = ['name','admin_id']