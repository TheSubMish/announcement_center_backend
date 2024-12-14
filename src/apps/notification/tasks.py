from celery import shared_task

from src.apps.announcement.models import Announcement, AnnouncementComment, AnnouncementLike
from src.apps.notification.models import Notification, NotificationType
from src.apps.notification.serializers import NotificationSerializer
from src.apps.notification.consumers import send_notification
from src.apps.auth.models import User

@shared_task
def announcement_creation_notification(annoucement_id, type: str):

    try:

        announcement = Announcement.objects.get(id=annoucement_id)
        recipients = [
            user
            for user in User.objects.filter(groupmember__group=announcement.group).exclude(pk=announcement.user.pk)
        ]

        if type == "create":
            notification_type = NotificationType.ANNOCUNCEMENT_CREATE
        elif type == "update":
            notification_type = NotificationType.ANNOUNCEMENT_UPDATE
        elif type == "comment":
            notification_type = NotificationType.ANNOUNCEMENT_COMMENT_CREATE
        elif type == "like":
            notification_type = NotificationType.ANNOUNCEMENT_LIKE
        elif type == "unlike":
            notification_type = NotificationType.ANNOUNCEMENT_UNLIKE
        else:
            return "Invalid type"

        for recipient in recipients:
            notification =  Notification.objects.create(
                sender=announcement.user,
                receiver=recipient,
                type=notification_type,
                message=f"{announcement.id}",
                read=False,
            )

            data = NotificationSerializer(instance=notification).data

            payload = {
                "type": "notify",
                "data": {"type": "notification", "notification": data},
                "group_names": [f"notifications_{str(notification.receiver.pk)}"], # type: ignore
            }

            send_notification(
                payload=payload
            )

    except Exception as e:
        return str(e)


@shared_task
def announcement_comment_notification(annoucement_comment_id, type: str):

    try:

        announcement_comment = AnnouncementComment.objects.get(id=annoucement_comment_id)

        if type == "comment":
            notification_type = NotificationType.ANNOUNCEMENT_COMMENT_CREATE
        else:
            return "Invalid type"

        notification =  Notification.objects.create(
            sender=announcement_comment.user,
            receiver=announcement_comment.announcement.user,
            type=notification_type,
            message=f"{announcement_comment.announcement.id}",
            read=False,
        )

        data = NotificationSerializer(instance=notification).data

        payload = {
            "type": "notify",
            "data": {"type": "notification", "notification": data},
            "group_names": [f"notifications_{str(notification.receiver.pk)}"], # type: ignore
        }

        send_notification(
            payload=payload
        )

    except Exception as e:
        return str(e)


@shared_task
def announcement_like_unlike_notification(annoucement_like_id, type: str):

    try:

        announcement_like_unlike = AnnouncementLike.objects.get(id=annoucement_like_id)

        if type == "like":
            notification_type = NotificationType.ANNOUNCEMENT_LIKE
        elif type == "dislike":
            notification_type = NotificationType.ANNOUNCEMENT_UNLIKE
        else:
            return "Invalid type"

        notification =  Notification.objects.create(
            sender=announcement_like_unlike.user,
            receiver=announcement_like_unlike.announcement.user,
            type=notification_type,
            message=f"{announcement_like_unlike.announcement.id}",
            read=False,
        )

        data = NotificationSerializer(instance=notification).data

        payload = {
            "type": "notify",
            "data": {"type": "notification", "notification": data},
            "group_names": [f"notifications_{str(notification.receiver.pk)}"], # type: ignore
        }

        send_notification(
            payload=payload
        )

    except Exception as e:
        return str(e)
