from django.conf import settings
from .mongodb import database
import uuid
import datetime
from django.db.models.signals import post_save
from src.apps.announcement.models import Announcement
from src.apps.group.models import GroupMember
from bson import Binary, UuidRepresentation

def notification(sender,instance,created,**kwargs):
    if created:
        db = database.connect_db(settings.MONGODB)
        group_members = GroupMember.objects.filter(group = instance.group).exclude(user=instance.user)
        notifications = []

        for group_member in group_members:
            notification = {
                "_id": Binary.from_uuid(uuid.uuid4(), UuidRepresentation.STANDARD),
                "sender": instance.user.id,
                "receiver": group_member.user.id,
                "message": f"{instance.user.username} created a announcement",
                "read": False,
                "created_at": datetime.datetime.now(),
            }
            notifications.append(notification)

        db.notification.insert_many(notifications)

post_save.connect(notification,sender=Announcement)