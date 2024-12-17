from django.db import models
from src.apps.group.models import AnnouncementGroup
from src.apps.announcement.models import Announcement
from src.apps.auth.models import User
# from src.apps.auth.models import User

# Create your models here.
class GroupImpression(models.Model):
    group = models.ForeignKey(AnnouncementGroup, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)


class AnnouncementImpression(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)