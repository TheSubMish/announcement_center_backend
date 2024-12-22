from rest_framework import serializers


class ImpressionSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    date = serializers.DateField()
    # country = serializers.CharField(max_length=50,required=False)
    # city = serializers.CharField(max_length=50,required=False)

    # def get_date(self, obj):
    #     # Format the date as a string (e.g., "YYYY-MM-DD")
    #     return obj['date'].strftime('%Y-%m-%d')

class AnnouncementLikeDislikeSerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()