from django.contrib import admin
from .models import AnnouncementGroup,Rating,GroupMember,Category
from django.contrib.auth.models import Group
# Register your models here.
@admin.register(AnnouncementGroup)
class AnnouncementGroupAdmin(admin.ModelAdmin):
    list_display = ['group_id','name','admin','status','created_at']
    ordering = ('-created_at',)
    search_fields = ['name','admin']
admin.site.unregister(Group)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['group','user','rating','status','created_at']
    ordering = ('-created_at',)
    search_fields = ['group','user']

@admin.register(GroupMember)
class GroupMemberShipAdmin(admin.ModelAdmin):
    list_display = ['id','group','user','status','role']
    ordering = ('-created_at',)
    search_fields = ['group','user','role']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_by','status','created_at']
    ordering = ('-created_at',)
    search_fields = ['name','created_by']