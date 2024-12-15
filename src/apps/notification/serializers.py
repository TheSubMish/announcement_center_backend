from rest_framework import serializers
from src.apps.auth.serializers import UserSerializer

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = "__all__"


class NotificationReadSerializer(serializers.ModelSerializer):
    # sender = UserSerializer(fields=["id","username"])
    # receiver = UserSerializer(fields=["id","username"])

    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_sender(self,obj):
        return UserSerializer(instance=obj.sender, fields=["id","username"]).data
    
    def get_receiver(self,obj):
        return UserSerializer(instance=obj.receiver, fields=["id","username"]).data

# class NotificationSerializer(serializers.Serializer):
#     _id = serializers.UUIDField()
#     sender = serializers.UUIDField()
#     receiver = serializers.UUIDField()
#     message = serializers.CharField(max_length=255)
#     read = serializers.BooleanField(default=False)
#     created_at = serializers.DateTimeField()

# class ReadNotificationSerializer(serializers.Serializer):
#     notification_id = serializers.UUIDField()
#     read = serializers.BooleanField(default=True)