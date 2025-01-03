from django.contrib import admin
from .models import Announcement,AnnouncementComment, AnnouncementLike, AnnouncementInterested
# Register your models here.
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['id','title','user','status','created_at']
    ordering = ('-created_at',)
    search_fields = ['title','admin']

@admin.register(AnnouncementComment)
class AnnouncementCommentAdmin(admin.ModelAdmin):
    list_display = ['id','announcement','user','status','created_at']
    ordering = ('-created_at',)
    search_fields = ['announcement','user']

@admin.register(AnnouncementLike)
class AnnouncementLikeAdmin(admin.ModelAdmin):
    list_display = ['id','announcement','user','like','dislike','status','created_at']
    ordering = ('-created_at',)
    search_fields = ['announcement','user']


@admin.register(AnnouncementInterested)
class AnnouncementInterestedAdmin(admin.ModelAdmin):
    list_display = ['id','announcement','user','interested','status','created_at']
    ordering = ('-created_at',)
    search_fields = ['announcement','user']
