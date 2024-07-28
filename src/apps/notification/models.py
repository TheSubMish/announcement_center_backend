from django.conf import settings
from .mongodb import database
import uuid
import datetime
from django.db.models.signals import post_save
from src.apps.announcement.models import Announcement,AnnouncementComment
from src.apps.group.models import GroupMember
from bson import Binary, UuidRepresentation

import logging
logger = logging.getLogger('error_logger')

def notification(sender,instance,created,**kwargs):

    try:
        db = database.connect_db(settings.MONGODB)
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return

    if created:
        if sender == Announcement:
            try:
                group_members = GroupMember.objects.filter(group = instance.group).exclude(user=instance.user)
                notifications = []

                for group_member in group_members:
                    notification = {
                        "_id": Binary.from_uuid(uuid.uuid4(), UuidRepresentation.STANDARD),
                        "sender": instance.user.id,
                        "receiver": group_member.user.id,
                        "message": f"{instance.user.username} created a announcement : {instance.id}'",
                        "read": False,
                        "created_at": datetime.datetime.now(),
                    }
                    notifications.append(notification)

                db.notification.insert_many(notifications)

            except Exception as e:
                logger.error(f"Failed to create notification: {e}")
                return
        
        elif sender == AnnouncementComment:
            try:
                notification = {
                    "_id": Binary.from_uuid(uuid.uuid4(), UuidRepresentation.STANDARD),
                    "sender": instance.user.id,
                    "receiver": instance.announcement.user.id,
                    "message": f"{instance.user.username} commented on your announcement : {instance.announcement}",
                    "read": False,
                    "created_at": datetime.datetime.now(),
                }
                db.notification.insert_one(notification)
            except Exception as e:
                logger.error(f"Failed to create notification: {e}")
                return

post_save.connect(notification,sender=Announcement)
post_save.connect(notification,sender=AnnouncementComment)