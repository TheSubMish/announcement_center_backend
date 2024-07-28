from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    _id = serializers.UUIDField()
    sender = serializers.UUIDField()
    receiver = serializers.UUIDField()
    message = serializers.CharField(max_length=255)
    read = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField()

class ReadNotificationSerializer(serializers.Serializer):
    notification_id = serializers.UUIDField()
    read = serializers.BooleanField(default=True)