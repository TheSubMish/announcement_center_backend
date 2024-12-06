from django.conf import settings
from .mongodb import database
import uuid
import datetime
from django.db.models.signals import post_save
from src.apps.announcement.models import Announcement,AnnouncementComment
from src.apps.group.models import GroupMember
from bson import Binary, UuidRepresentation
from src.apps.auth.models import User

import logging
logger = logging.getLogger('error_logger')

from django.db import models

class NotificationType(models.TextChoices):
    GROUP_JOIN = 'group_join','Group Join'
    GROUP_LEAVE = 'group_leave','Group Leave'
    ANNOCUNCEMENT_CREATE = 'announcement_create','Announcement Create'
    ANNOUNCEMENT_UPDATE = 'announcement_update','Announcement Update'
    ANNOUNCEMENT_COMMENT_CREATE = 'announcement_comment_create','Announcement Comment Create'
    ANNOUNCEMENT_LIKE = 'announcement_like','Announcement Like'
    ANNOUNCEMENT_UNLIKE = 'announcement_unlike','Announcement Unlike'

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    sender = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name="sender")
    receiver = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name="receiver")
    type = models.CharField(max_length=100, choices=NotificationType.choices,default=NotificationType.GROUP_JOIN)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# def notification(sender,instance,created,**kwargs):

#     try:
#         db = database.connect_db(settings.MONGODB)
#     except Exception as e:
#         logger.error(f"Failed to connect to MongoDB: {e}")
#         return

#     if created:
#         if sender == Announcement:
#             try:
#                 group_members = GroupMember.objects.filter(group = instance.group).exclude(user=instance.user)
#                 notifications = []

#                 for group_member in group_members:
#                     notification = {
#                         "_id": Binary.from_uuid(uuid.uuid4(), UuidRepresentation.STANDARD),
#                         "sender": instance.user.id,
#                         "receiver": group_member.user.id,
#                         "message": f"{instance.user.username} created a announcement : {instance.id}'",
#                         "read": False,
#                         "created_at": datetime.datetime.now(),
#                     }
#                     notifications.append(notification)

#                 db.notification.insert_many(notifications)

#             except Exception as e:
#                 logger.error(f"Failed to create notification: {e}")
#                 return
        
#         elif sender == AnnouncementComment:
#             try:
#                 notification = {
#                     "_id": Binary.from_uuid(uuid.uuid4(), UuidRepresentation.STANDARD),
#                     "sender": instance.user.id,
#                     "receiver": instance.announcement.user.id,
#                     "message": f"{instance.user.username} commented on your announcement : {instance.announcement}",
#                     "read": False,
#                     "created_at": datetime.datetime.now(),
#                 }
#                 db.notification.insert_one(notification)
#             except Exception as e:
#                 logger.error(f"Failed to create notification: {e}")
#                 return

# post_save.connect(notification,sender=Announcement)
# post_save.connect(notification,sender=AnnouncementComment)