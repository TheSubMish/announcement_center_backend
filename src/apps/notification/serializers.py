from rest_framework import serializers
from src.apps.auth.serializers import UserSerializer
from src.apps.group.serializers import AnnouncementGroupSerializer

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = "__all__"


class NotificationReadSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    announcement = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_sender(self,obj):
        return UserSerializer(instance=obj.sender, fields=["id","username"]).data
    
    def get_receiver(self,obj):
        return UserSerializer(instance=obj.receiver, fields=["id","username"]).data
    
    def get_announcement(self,obj):
        from src.apps.announcement.serializers import AnnouncementSerializer

        if obj.announcement:
            return AnnouncementSerializer(instance=obj.announcement, fields=["id","title"]).data
        else:
            return None
        
    def get_group(self,obj):
        if obj.group:
            return AnnouncementGroupSerializer(instance=obj.group, fields=["id","name","category"]).data
        else:
            return None

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