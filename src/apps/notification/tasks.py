from celery import shared_task

from src.apps.announcement.models import Announcement, AnnouncementComment, AnnouncementLike
from src.apps.group.models import Rating, GroupMember
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
                announcement = announcement,
                group = announcement.group,
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
            announcement = announcement_comment.announcement,
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
            announcement = announcement_like_unlike.announcement,
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


@shared_task
def group_join_leave_kick_notification(group_id, type: str):

    try:

        group_member = GroupMember.objects.get(group__group_id=group_id)

        if type == "group_join":
            notification_type = NotificationType.GROUP_JOIN
        elif type == "group_leave":
            notification_type = NotificationType.GROUP_LEAVE
        elif type == "group_kick":
            notification_type = NotificationType.GROUP_KICK
        else:
            return "Invalid type"

        notification =  Notification.objects.create(
            group = group_member.group,
            sender=group_member.user,
            receiver=group_member.group.admin,
            type=notification_type,
            message=f"{group_member.group.pk}",
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
def group_rating_notification(rate_id, type: str):

    try:

        group_rate = Rating.objects.get(id=rate_id)

        if type == "group_rate":
            notification_type = NotificationType.GROUP_RATE
        else:
            return "Invalid type"

        notification =  Notification.objects.create(
            group = group_rate.group,
            sender=group_rate.user,
            receiver=group_rate.group.admin,
            type=notification_type,
            message=f"{group_rate.group.pk}",
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
