from rest_framework import serializers


class ImpressionSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    date = serializers.DateTimeField()
    country = serializers.CharField(max_length=50,required=False)
    city = serializers.CharField(max_length=50,required=False)

class AnnouncementLikeDislikeSerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()