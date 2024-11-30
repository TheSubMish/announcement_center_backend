from celery import shared_task

from src.apps.announcement.models import Announcement
from src.apps.notification.models import Notification
from src.apps.notification.serializers import NotificationSerializer
from src.apps.notification.consumers import send_notification
from src.apps.auth.models import User

@shared_task
def announcement_creation_notification(annoucement_id):

    try:

        announcement = Announcement.objects.get(id=annoucement_id)
        recipients = [
            user
            for user in User.objects.filter(groupmember__group=announcement.group).exclude(pk=announcement.user.pk)
        ]

        for recipient in recipients:
            notification =  Notification.objects.create(
                sender=announcement.user,
                receiver=recipient,
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


        # subject = f"New announcement created: {announcement.title}"
        # message = f"User {announcement.user.username} has created a new announcement: {announcement.title}"

        # notification = Notification(
        #     sender=announcement.user,
        #     receiver=None,
        #     message=message,
        #     read=False,
        # )
        # notification.save()

    except Exception as e:
        return str(e)