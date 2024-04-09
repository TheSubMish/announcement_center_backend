from django.contrib import admin
from .models import Announcement
# Register your models here.
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['id','title','admin','paid_for_email','created_at']
    ordering = ('-created_at',)
    search_fields = ['title','admin']
