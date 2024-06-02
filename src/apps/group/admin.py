from django.contrib import admin
from .models import AnnouncementGroup,Rating,GroupMember
# Register your models here.
@admin.register(AnnouncementGroup)
class AnnouncementGroupAdmin(admin.ModelAdmin):
    list_display = ['group_id','name','admin_id','created_at']
    ordering = ('-created_at',)
    search_fields = ['name','admin_id']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['group','user','rating','created_at']
    ordering = ('-created_at',)
    search_fields = ['group','user']

@admin.register(GroupMember)
class GroupMemberShipAdmin(admin.ModelAdmin):
    list_display = ['id','group','user','role']
    ordering = ('-created_at',)
    search_fields = ['group','user','role']