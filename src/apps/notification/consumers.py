from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from src.apps.auth.models import User
from django.contrib.auth.models import AnonymousUser
from src.apps.notification.models import Notification

import json

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        try:
            if not self.scope["user"] or isinstance(self.scope["user"], AnonymousUser):
                self.close(code=4001)

                return

            self.user: User = self.scope["user"]

            self.group_name = "notifications_{user_id}".format(
                user_id=self.user.id
            )

            print(self.group_name)

            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)  # type: ignore
            self.accept()

        except Exception as err:

            return

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(  # type: ignore
                self.group_name, self.channel_name
            )
        except Exception as err:
            return

    def receive(self, text_data=None, bytes_data=None):
        try:
            if not text_data:
                return

            data = json.loads(text_data)
            if data.get("action") == "seen":
                _db = self.user._state.db
                try:
                    notification: Notification = Notification.objects.get(
                        id=data.get("notification_id")
                    )
                except Notification.DoesNotExist:
                    return

        except Exception as err:
            return

    def notify(self, event: dict):
        try:
            self.send(text_data=json.dumps(event.get("data")))
        except Exception as err:
            return