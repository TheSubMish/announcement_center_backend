from typing import Any
from django.db import models
from src.apps.common.models import BaseModel,Status
from src.apps.common.utills import image_validate
from src.apps.auth.models import UserModelMixin,User
from src.apps.group.models import GroupModelMixin
from django_ckeditor_5.fields import CKEditor5Field

class AnnouncementType(models.TextChoices):
    EVENT = 'event','Event'
    NEWS = 'news','News'
    UPDATE = 'update','Update'
    OFFER = 'offer','Offer'
    PRODUCTLAUNCH = 'product launch','Product Launch'
    TRAINING = 'training','Training'
    BOOTCAMPS = 'bootcamp','Bootcamp'

class AnnouncementVisibilty(models.TextChoices):
    PUBLIC = 'public','Public'
    PRIVATE = 'private','Private'

class Announcement(BaseModel,UserModelMixin,GroupModelMixin):
    title = models.CharField(max_length=255,null=False, blank=False)
    description = CKEditor5Field('Description',config_name='extends')
    image = models.ImageField(null=False,blank=False,validators=[image_validate],upload_to='announcement')
    location = models.CharField(max_length=255,null=True, blank=True)

    link = models.URLField(null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)

    announcement_visibility = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=AnnouncementVisibilty.choices,
        default=AnnouncementVisibilty.PUBLIC,
    )
    announcement_type = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=AnnouncementType.choices,
        default=AnnouncementType.EVENT,
    )
    
    date = models.DateField(null=True, blank=True)
    image_description = models.TextField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.status = Status.INACTIVE
        self.save()
    
    def __str__(self):
        return self.title
    
class AnnouncementComment(BaseModel):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=255, null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # Nested comment structure

    def __str__(self):
        if self.user:
            prefix = "  " * self.get_level()  # Indentation based on nesting level
            return f"{prefix}{self.user.username} - {self.comment[:20]}"  # Truncated comment preview
        else:
            prefix = "  " * self.get_level()
            return f"{prefix}Anonymous - {self.comment[:20]}"

    def get_level(self):
        """Calculates the nesting level of the comment (root = 0)"""
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
    
    def delete(self, *args, **kwargs):
        self.status = Status.INACTIVE
        self.save()